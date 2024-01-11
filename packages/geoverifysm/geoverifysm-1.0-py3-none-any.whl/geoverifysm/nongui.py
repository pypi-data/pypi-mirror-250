import copy
import json
import os.path
import time
import openai
import numpy as np
import itertools

import pandas as pd
from transformers import pipeline

from .langchain_booth.baselines import LargestCommonPrefix, RandomRollout
from .langchain_booth.overlap import natual_language_overlap, tool_overlap
from .scraper.level_scraper import decompose_example


def group_results(data, rank):
    if rank == 1:
        a = data['Coverage NL']['pass@1']
        b = data['Exact Tool']['pass@1']
        c = data['Exact ToolSym HardSeq:False']['pass@1']
    else:
        a = data['Coverage NL']['pass@50']
        b = data['Exact Tool']['pass@50']
        c = data['Exact ToolSym HardSeq:False']['pass@50']
    return (a + b + c) / 3


def subsol(series_ws, series):
    series_ws = series_ws.values
    series = series.values
    results = []
    for x, y in zip(series_ws, series):
        results.append([x[len(y):]])
    return results


def populate(somelist, n=20):
    new_list = []
    for i in somelist:
        new_list.append([i] * n)
    return new_list


def estimate_pass_at_k(
        num_samples,
        num_correct,
        k,
) -> np.ndarray:
    """
    Estimates pass@k of each problem and returns them in an array.
    """

    def estimator(n: int, c: int, k: int) -> float:
        """
        Calculates 1 - comb(n - c, k) / comb(n, k).
        """
        if n - c < k:
            return 1.0
        return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

    if isinstance(num_samples, int):
        num_samples_it = itertools.repeat(num_samples, len(num_correct))
    else:
        assert len(num_samples) == len(num_correct)
        num_samples_it = iter(num_samples)

    return np.array([estimator(int(n), int(c), k) for n, c in zip(num_samples_it, num_correct)])


def find_index_ranges(df, column_name):
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame")

    # Dictionary to store the ranges
    ranges = {}

    # Initial variables
    prev_value = None
    start_index = None

    for i, row in df.iterrows():
        # Check for change in category
        if row[column_name] != prev_value:
            # If not the first category, save the previous category's range
            if prev_value is not None:
                ranges[prev_value] = [start_index, i - 1]

            # Update for new category
            prev_value = row[column_name]
            start_index = i

    # Add the last category's range
    if prev_value is not None:
        ranges[prev_value] = [start_index, df.index[-1]]

    return ranges


def match_index_with_pack(i, reverse_pack_dict):
    for v, k in reverse_pack_dict.items():
        real_v = eval(v)
        if i in range(real_v[0], real_v[1] + 1):
            return k


class GeometryEvaluator:

    def __init__(self, dataset, results, model, results_tools=None, results_symbols=None, prompt=None):
        """
        Initializes the GeometryEvaluator with a dataset and model.

        Args:
        - dataset: A list of strings.
        - results: A list of generated responses.
        - results_symbols: A list of generates symbols per response.
        - model: A string representing either an OpenAI model or a HuggingFace model on the hub.
        - prompt: A prompt (inception prompt) to be appended before the model.
        """
        self.prompt = prompt if prompt is not None else ''
        self.dataset = dataset
        self.pack_list = {str(v): k for k, v in find_index_ranges(dataset, 'pack').items()}

        if isinstance(results, np.ndarray):
            results = list(results)
        if isinstance(results_tools, np.ndarray):
            results_tools = list(results_tools)
        if isinstance(results_symbols, np.ndarray):
            results_symbols = list(results_symbols)
        if isinstance(results, list):
            self.results = results
            assert results_tools is not None
            assert results_symbols is not None
            self.results_tools = results_tools
            self.results_symbols = results_symbols
        elif isinstance(results, pd.DataFrame):
            self.results = results['solution']
            self.results_tools = results['solution_tool']
            self.results_symbols = results['solution_symbol']
        elif isinstance(results, dict):
            self.results = []
            self.results_tools = []
            self.results_symbols = []
            self.prepare_results(results['results'])
        else:
            self.results = None
            if "gpt" in model or "davinci" in model:  # Check for OpenAI model
                self.model_type = "openai"
                self.model_name = model
            elif "/" in model:  # Assume it's a HuggingFace model
                self.model_type = "huggingface"
                self.generator = pipeline("text-generation", model=model)
            else:
                self.model_type = None
                self.generator = None
            return

        # Level 1 fix #
        if isinstance(self.results[0], str):
            self.results = [[f] for f in self.results]

        if isinstance(self.results_tools[0], str):
            self.results_tools = [[eval(f)] for f in self.results_tools]

        if isinstance(self.results_symbols[0], str):
            self.results_symbols = [[eval(f)] for f in self.results_symbols]

        # Level 2 fix #
        if isinstance(self.results[0], list) and isinstance(self.results[0][0], str):
            pass

        if isinstance(self.results_tools[0], list) and isinstance(self.results_tools[0][0], str):
            final_result = []
            for k in self.results_tools:
                instance_result = []
                for f in k:
                    instance_result.append(eval(f))
                final_result.append(instance_result)
            self.results_tools = final_result

        if isinstance(self.results_symbols[0], list) and isinstance(self.results_symbols[0][0], str):
            final_result = []
            for k in self.results_symbols:
                instance_result = []
                for f in k:
                    instance_result.append(eval(f))
                final_result.append(instance_result)
            self.results_symbols = final_result

    def generate(self, top_p=0.99, temperature=1.0, number_of_generations=5, cont=False):
        """
        Evaluate the dataset using the model and get the generated tokens.

        Args:
        - top_p: A float representing the nucleus sampling.
        - temperature: A float representing the randomness of the generation.
        - number_of_generations: An integer representing how many times to generate a response for each example.
        - cont: Whether to continue from a previous example.

        Returns:
        - results: A list containing generated responses.
        """
        completed = 0
        lookfor = f'{self.model_name}_{number_of_generations}.json'
        if cont:
            c_lookfor = [f for f in os.listdir('.') if
                         '.json' in f and self.model_name in f and str(number_of_generations) in f and 'outof' in f]
            if len(c_lookfor) > 0:
                lookfor = c_lookfor[0]
                completed = int(lookfor.split('_')[2])
                print(f"Continue Experiment with model: {self.model_name}\n")
                print(f"With N: {number_of_generations}\n")
                print(f"Completed: {completed}\n")
            else:
                pass
        if os.path.exists(lookfor) and not cont:
            with open(lookfor, 'r') as fin:
                results = json.load(fin)['results']
        else:
            results = []
            total_length = len(self.dataset['question'])
            for i, text in enumerate(self.dataset['question']):
                if i < completed:
                    continue
                if self.model_type == "openai":
                    ### Temporary Code ###
                    final_text = self.prompt + '\n\nProblem:\n' + text
                    ######################
                    try:
                        if '4' in self.model_name:
                            # GPT4 needs another API CALL#
                            # Fix name #
                            if '__' in self.model_name:
                                run_name = self.model_name.split('__')[1]
                            else:
                                run_name = self.model_name
                            response = openai.ChatCompletion.create(
                                model=run_name,
                                temperature=temperature,
                                top_p=top_p,
                                max_tokens=200,
                                n=number_of_generations,
                                stop=['\n\n'],
                                messages=
                                [{
                                    "role": "user",
                                    "content": final_text
                                }]
                            )
                            generated_text = [f.message.content for f in response.choices]
                            time.sleep(1)
                        else:
                            if '__' in self.model_name:
                                run_name = self.model_name.split('__')[1]
                            else:
                                run_name = self.model_name
                            response = openai.Completion.create(
                                engine=run_name,
                                prompt=final_text,
                                max_tokens=200,
                                top_p=top_p,
                                temperature=temperature,
                                n=number_of_generations,
                                stop=['\n\n']
                            )
                            generated_text = [f.text for f in response.choices]
                    except Exception as e:
                        print(e)
                        # AT ANY TIMEOUT / RATE ERROR --> cashout #
                        completed_so_far = len(results)
                        with open(
                                f'{self.model_name}_{number_of_generations}_{completed_so_far}_outof_{total_length}.json',
                                'w') as fout:
                            json.dump({'results': results}, fout)
                        return
                elif self.model_type == "huggingface":  # Use HuggingFace model
                    ### Temporary Code ###
                    final_text = self.prompt + '\n\nProblem:\n' + text
                    ######################
                    generated_text = \
                        self.generator(final_text, top_p=top_p, temperature=temperature, n=number_of_generations)[0][
                            'generated_text']
                    generated_text = generated_text[len(final_text):].strip()  # Only keep the generated portion
                else:
                    raise ValueError("You cant generate with None model...")
                results.append(generated_text)
        # assert len(self.dataset) == len(results) + completed
        assert len(results[0]) == len(results[-1]) == number_of_generations
        with open(f'{self.model_name}_{number_of_generations}.json', 'w') as fout:
            json.dump({'results': results}, fout)

        ### Post process results into the required dataset format ###
        print("Formatting results...")
        self.results = []
        self.results_tools = []
        self.results_symbols = []
        for problem_instance, initial_symbols in zip(results, self.dataset['initial_symbol']):
            instance_responses = []
            instance_tools = []
            instance_symbols = []
            for generated_solution in problem_instance:
                # Some responses can be trash so filter them #
                if len(generated_solution) < 5:
                    continue
                response_solution, (response_tools, response_symbols) = decompose_example(solution=generated_solution,
                                                                                          initial_symbols=eval(
                                                                                              initial_symbols))
                instance_responses.append(response_solution)
                instance_tools.append(response_tools)
                instance_symbols.append(response_symbols)
            self.results.append(instance_responses)
            self.results_tools.append(instance_tools)
            self.results_symbols.append(instance_symbols)
        return

    def test_1(self, pack_list=None, threshold=0.62):
        raw_scores = []
        pack_results = {}
        # Find the n factor (n/k)
        examples = len(self.results)
        active_examples = 0
        for i in range(examples):
            pack_as_string = match_index_with_pack(i, self.pack_list)
            if pack_list is None or pack_as_string not in pack_list:
                continue
            if pack_as_string == 'Alpha':
                # TODO: FIX THIS BUG CAUSED BY MISMATCH OF TUTORIAL AND ALPHA
                threshold = 0.5
            active_examples += 1
            attempts_per_example = len(self.results[i])
            r = 0
            for j in range(attempts_per_example):
                scores = natual_language_overlap(self.results[i][j], self.dataset['solution_nl'].values[i])
                raw_scores.append(scores)
                scores_ = 1.0 * (scores > threshold)
                r += scores_
            pass1 = estimate_pass_at_k([attempts_per_example], [r], 1).mean()
            pass50 = estimate_pass_at_k([attempts_per_example], [r], attempts_per_example).mean()
            if pack_as_string not in pack_results:
                pack_results.update(
                    {pack_as_string: {'Coverage NL': {'pass@1': pass1, 'pass@50': pass50}}})
            else:
                pack_results[pack_as_string]['Coverage NL']['pass@1'] += pass1
                pack_results[pack_as_string]['Coverage NL']['pass@50'] += pass50

        ### PACK AVERAGE ###
        pass1_all = 0
        pass50_all = 0
        if pack_list is None:
            pack_list = [(k, eval(v)[1] - eval(v)[0] + 1) for v, k in self.pack_list.items()]
        else:
            pack_list = [(k, eval(v)[1] - eval(v)[0] + 1) for v, k in self.pack_list.items() if k in pack_list]
        for p, r in pack_list:
            if p not in pack_results:
                continue
            pack_results[p]['Coverage NL']['pass@1'] = pack_results[p]['Coverage NL']['pass@1'] / r
            pass1_all += pack_results[p]['Coverage NL']['pass@1'] * (1 / len(pack_list))
            pack_results[p]['Coverage NL']['pass@50'] = pack_results[p]['Coverage NL']['pass@50'] / r
            pass50_all += pack_results[p]['Coverage NL']['pass@50'] * (1 / len(pack_list))
        ### AVERAGE OVER ALL ###
        return {'Coverage NL': {'pass@1': pass1_all,
                                'pass@50': pass50_all}}

    def test_2(self, pack_list=None, threshold=3):
        raw_scores = []
        pack_results = {}
        # Find the n factor (n/k)
        examples = len(self.results_tools)
        active_examples = 0
        for i in range(examples):
            pack_as_string = match_index_with_pack(i, self.pack_list)
            if pack_list is None or pack_as_string not in pack_list:
                continue
            active_examples += 1
            attempts_per_example = len(self.results_tools[i])
            r = 0
            for j in range(attempts_per_example):
                scores = tool_overlap(response=self.results_tools[i][j],
                                      ground_truth=eval(self.dataset['solution_tool'].values[i]))
                raw_scores.append(scores)
                scores = 1.0 * (scores < threshold)
                r += scores
            pass1 = estimate_pass_at_k([attempts_per_example], [r], 1).mean()
            pass50 = estimate_pass_at_k([attempts_per_example], [r], attempts_per_example).mean()
            if pack_as_string not in pack_results:
                pack_results.update(
                    {pack_as_string: {'Exact Tool': {'pass@1': pass1, 'pass@50': pass50}}})
            else:
                pack_results[pack_as_string]['Exact Tool']['pass@1'] += pass1
                pack_results[pack_as_string]['Exact Tool']['pass@50'] += pass50

        ### PACK AVERAGE ###
        pass1_all = 0
        pass50_all = 0
        if pack_list is None:
            pack_list = [(k, eval(v)[1] - eval(v)[0] + 1) for v, k in self.pack_list.items()]
        else:
            pack_list = [(k, eval(v)[1] - eval(v)[0] + 1) for v, k in self.pack_list.items() if k in pack_list]
        for p, r in pack_list:
            if p not in pack_results:
                continue
            pack_results[p]['Exact Tool']['pass@1'] = pack_results[p]['Exact Tool']['pass@1'] / r
            pass1_all += pack_results[p]['Exact Tool']['pass@1'] * (1 / len(pack_list))
            pack_results[p]['Exact Tool']['pass@50'] = pack_results[p]['Exact Tool']['pass@50'] / r
            pass50_all += pack_results[p]['Exact Tool']['pass@50'] * (1 / len(pack_list))
        ### AVERAGE OVER ALL ###
        return {'Exact Tool': {'pass@1': pass1_all / active_examples,
                               'pass@50': pass50_all / active_examples}}

    def test_3(self, pack_list=None, threshold=3, hardseq=False):
        raw_scores = []
        pack_results = {}
        # Find the n factor (n/k)
        examples = len(self.results_tools)
        active_examples = 0
        for i in range(examples):
            pack_as_string = match_index_with_pack(i, self.pack_list)
            if pack_list is None or pack_as_string not in pack_list:
                continue
            active_examples += 1
            attempts_per_example = len(self.results_tools[i])
            r = 0
            for j in range(attempts_per_example):
                scores = tool_overlap(response=self.results_tools[i][j],
                                      response_sym=self.results_symbols[i][j],
                                      ground_truth=eval(self.dataset['solution_tool'].values[i]),
                                      ground_truth_sym=eval(self.dataset['solution_symbol'].values[i]),
                                      hardseq=hardseq)
                raw_scores.append(scores)
                scores = 1.0 * (scores < threshold)
                r += scores
            pass1 = estimate_pass_at_k([attempts_per_example], [r], 1).mean()
            pass50 = estimate_pass_at_k([attempts_per_example], [r], attempts_per_example).mean()
            if pack_as_string not in pack_results:
                pack_results.update(
                    {pack_as_string: {
                        f'Exact ToolSym HardSeq:{hardseq}': {'pass@1': pass1, 'pass@50': pass50}}})
            else:
                pack_results[pack_as_string][f'Exact ToolSym HardSeq:{hardseq}']['pass@1'] += pass1
                pack_results[pack_as_string][f'Exact ToolSym HardSeq:{hardseq}']['pass@50'] += pass50
        ### PACK AVERAGE ###
        pass1_all = 0
        pass50_all = 0
        if pack_list is None:
            pack_list = [(k, eval(v)[1] - eval(v)[0] + 1) for v, k in self.pack_list.items()]
        else:
            pack_list = [(k, eval(v)[1] - eval(v)[0] + 1) for v, k in self.pack_list.items() if k in pack_list]
        for p, r in pack_list:
            if p not in pack_results:
                continue
            pack_results[p][f'Exact ToolSym HardSeq:{hardseq}']['pass@1'] = \
                pack_results[p][f'Exact ToolSym HardSeq:{hardseq}']['pass@1'] / r
            pass1_all += pack_results[p][f'Exact ToolSym HardSeq:{hardseq}']['pass@1'] * (1 / len(pack_list))
            pack_results[p][f'Exact ToolSym HardSeq:{hardseq}']['pass@50'] = \
                pack_results[p][f'Exact ToolSym HardSeq:{hardseq}']['pass@50'] / r
            pass50_all += pack_results[p][f'Exact ToolSym HardSeq:{hardseq}']['pass@50'] * (1 / len(pack_list))
        ### AVERAGE OVER ALL ###
        return {f'Exact ToolSym HardSeq:{hardseq}': {'pass@1': pass1_all / active_examples,
                                                     'pass@50': pass50_all / active_examples}}

    def evaluate(self, pack_list=None, **kwargs):
        """
        Performs analysis of results. Groups them by pack-name (optional like my will to live).
        1: Coverage Test NL (whether your generated NL steps include the NL solution steps)
        2: Exact Test Tool: Exact Match Tool
        3: Exact Test Tool + Symbols: Exact Match Tool and Symbol Count
        Final result is the smallest of the three.
        """
        if self.results is None:
            self.generate(**kwargs)
        final_results = {}
        final_results.update(self.test_1(pack_list=pack_list))
        final_results.update(self.test_2(pack_list=pack_list))
        final_results.update(self.test_3(pack_list=pack_list))
        pass_1 = group_results(final_results, 1)
        pass_50 = group_results(final_results, 50)

        print(pass_1, pass_50)
        return final_results

    def evaluate_lcs(self, pack_list=None):
        if self.results_tools is None:
            self.generate_random_baseline(random_name='lcs')
        final_results = {}
        final_results.update(self.test_2(pack_list=pack_list)[0])
        return final_results

    def evaluate_rollout(self, pack_list=None):
        if self.results_tools is None:
            self.generate_random_baseline(random_name='lcs')
        final_results = {}
        final_results.update(self.test_2(pack_list=pack_list)[0])
        final_results.update(self.test_3(pack_list=pack_list)[0])
        return final_results

    def generate_random_baseline(self, random_name='rnd', number_of_generations=1):
        lookfor = f'{random_name}_{number_of_generations}.json'
        if os.path.exists(lookfor):
            with open(lookfor, 'r') as fin:
                results = json.load(fin)['results']
        else:
            if random_name == 'lcp':
                engine = LargestCommonPrefix()
                engine.fit(self.dataset)
                results = engine.predict_all(self.dataset)
                self.results_tools = []
                for problem_instance in results:
                    instance_tools = []
                    for response_tools in problem_instance:
                        instance_tools.append(response_tools)
                    self.results_tools.append(instance_tools)
            elif random_name == 'rollout':
                engine = RandomRollout()
                engine.fit(self.dataset)
                tools, symbols = engine.predict_all(self.dataset)
                self.results_tools = []
                self.results_symbols = []
                for problem_instance in tools:
                    instance = []
                    for response in problem_instance:
                        instance.append(response)
                    self.results_tools.append(instance)
                    self.results_symbols.append(instance)
            else:
                raise NotImplementedError
        return

    def prepare_results(self, results):
        print("Formatting results and removing outliers...\n")
        results = results[:19]
        for problem_instance, initial_symbols in zip(results, self.dataset['initial_symbol']):
            instance_responses = []
            instance_tools = []
            instance_symbols = []
            for generated_solution in problem_instance:
                # Some responses can be trash so filter them #
                if len(generated_solution) < 50:
                    continue
                response_solution, (response_tools, response_symbols) = decompose_example(solution=generated_solution,
                                                                                          initial_symbols=eval(
                                                                                              initial_symbols))
                instance_responses.append(response_solution)
                instance_tools.append(response_tools)
                instance_symbols.append(response_symbols)
            self.results.append(instance_responses)
            self.results_tools.append(instance_tools)
            self.results_symbols.append(instance_symbols)


def table_3_experiment(dataset, results):
    evaulator = GeometryEvaluator(dataset=dataset, results=results,
                                  results_tools=None,
                                  results_symbols=None,
                                  model=None)

    return evaulator.evaluate(pack_list=['Alpha', 'Beta'])


if __name__ == '__main__':
    dataset = pd.read_csv('../test/filtered_euclidea.csv').dropna().reset_index(drop=True).drop(columns=['Unnamed: 0'])
    with open('../test/results.json', 'r') as fin:
        results = json.load(fin)

    evaulator = GeometryEvaluator(dataset=dataset, results=results,
                                  results_tools=None,
                                  results_symbols=None,
                                  model=None)

    evaulator.evaluate(pack_list=['Alpha', 'Beta'])
