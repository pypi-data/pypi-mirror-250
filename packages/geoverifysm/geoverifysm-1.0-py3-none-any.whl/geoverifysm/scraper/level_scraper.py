import copy
import Levenshtein
import numpy as np
import re
from .constants import TOOL2IDX, IDX2TOOL
from .utils import get_symbols, compare_symbols


def format_question(question, qs):
    """
    qs: Part of the solution that usually is an assumption starting with Let.
    We move this to the question instead.
    """
    if qs is not None:
        if question[-1] == '.' or question[-1] == '?':
            question += qs
        else:
            question = question.strip() + '. ' + qs

    question = question.strip()
    ### Look for symbols ###
    initial_symbols = get_symbols(question)
    return question, initial_symbols


def format_solutions(solution):
    """
    qs: Part of the solution that usually is an assumption starting with Let.
    We move this to the question instead.
    """
    kw = None
    if 'Let' in solution:
        kw = 'Let'
    elif 'Given' in solution:
        kw = 'Given'
    if kw is not None:
        start_idx = solution.find(kw)
        ### Fix for one weird level ###
        offset = solution.find('{\displaystyle AB>AO,AC>AO}')
        if offset != -1:
            qs = 'Let O be the vertex of the angle and A the given point. Let B, C be abitary points on each ray, such that AB is bigger than AO and  AC is bigger than AO.'
            solution = 'Construct circle O with center O and radius OA.\nConstruct circle B with center B and radius BA, intersecting circle O at F.\nConstruct circle B with center C and radius CA, intersecting circle O at G.\nConstruct line FG, intersecting line OB at H, intersecting line OC at I.\nConstruct line AH.\nConstruct line AI.'
            return solution, qs
        else:
            possible_end_idxs = [solution.find(f) for f in ['.', 'Construct', 'Draw', 'With', 'Point', 'Starting']]
            possible_end_idxs = min([f for f in possible_end_idxs if f != -1]) + 1
        qs = solution[start_idx:possible_end_idxs]
        solution_ = solution[possible_end_idxs:]
        if solution_.startswith('onstruct'):
            possible_end_idxs -= 1
            qs = solution[start_idx:possible_end_idxs].strip()
        solution = solution[possible_end_idxs:]
    else:
        qs = None
    solution = solution.replace('\n\n', '\n')
    return solution, qs


def check_word(word, sentence):
    pattern = r'\b' + re.escape(word) + r'\b'
    return bool(re.search(pattern, sentence, re.IGNORECASE))


def annotate_solutions(step_solutions, toolset, initial_symbols=None):
    """
    Annotates solutions according to the tool used.
    Keeps track of emitted symbols at each tool round
    Heuristic method.
    """

    keyword_2_tool = {
        'circle': ['Circle Tool'],
        'line': ['Line Tool'],
        'point': ['Point Tool'],
        'intersect': ['Intersect Tool'],
        'bisect': ['Perpendicular Bisector Tool', 'Angle Bisector Tool'],
        'midpoint': ['Perpendicular Bisector Tool', 'Perpendicular Tool'],
        'angle': ['Angle Bisector Tool'],
        'vertical': ['Perpendicular Tool'],
        'perpendicular': ['Perpendicular Bisector Tool', 'Perpendicular Tool'],
        'parallel': ['Parallel Tool'],
        'compass': ['Compass Tool'],
    }

    step_solutions = [f for f in step_solutions.split('\n') if len(f) > 2]
    num_solutions = len(step_solutions)
    refined_solutions = []
    gt_tools = []
    history_symbols = initial_symbols if initial_symbols is not None else []
    per_step_symbols = [copy.deepcopy(history_symbols)]
    for i in range(num_solutions):
        current_solution = copy.deepcopy(step_solutions[i])
        current_solution = current_solution.lower().strip()
        if ',' in current_solution:
            current_solution = current_solution[:current_solution.find(',')]
        ### Voting classifier ###
        possible_tools = np.zeros(shape=(9,))  # 9 Tools
        for keyword, tools in keyword_2_tool.items():
            if check_word(keyword, current_solution):
                for tool in tools:
                    if tool in toolset:
                        possible_tools[TOOL2IDX[tool]] += 1
        ### If no tool ###
        if np.sum(possible_tools) == 0:
            continue
        ### Take the smallest id as the most probable ###
        tool_name = IDX2TOOL[np.argmax(possible_tools)]
        refined_solutions.append(f'<{tool_name}>{step_solutions[i]}')
        gt_tools.append(tool_name)
        ### Now find (if any) associated points and resulting symbols from each operation ###
        emitted_symbols = get_symbols(step_solutions[i])
        new_symbols = compare_symbols(history_symbols, emitted_symbols)
        if len(new_symbols) > 0:
            history_symbols += new_symbols
        per_step_symbols.append(new_symbols)
    refined_solutions = '\n'.join(refined_solutions)
    return refined_solutions, gt_tools, per_step_symbols


def format_explanations(explanation):
    return explanation


def format_tools(tools):
    proper_tools = []
    distances = np.zeros(shape=(9,))
    for tool in tools:
        if tool == 'Move Tool':
            continue
        ### Look over the correct tools ###
        for proper_tool_name, proper_tool_idx in TOOL2IDX.items():
            distances[proper_tool_idx] = Levenshtein.distance(tool.lower(), proper_tool_name.lower())
        ### Find the tool with the correct (minimum distance) ###
        proper_tools.append(IDX2TOOL[np.argmin(distances)])
    return proper_tools


def make_example(question, solution, explanation, available_tools):
    if isinstance(solution, list):
        solution = solution[0]
    s, qs = format_solutions(solution)
    q, initial_symbols = format_question(question, qs)
    tools = format_tools(available_tools)
    s, gt_tools, gt_symbols = annotate_solutions(s, tools, copy.deepcopy(initial_symbols))
    e = format_explanations(explanation)
    problem = f"Description: {q}\n" \
              f"Tool List: {tools}\n" \
              f"Solution: "

    problem_with_solution = problem + s
    problem_with_rationale = problem_with_solution + f'\nRationale: {e}'
    return (problem, problem_with_solution, problem_with_rationale), (gt_tools, gt_symbols, initial_symbols)


def decompose_example(solution, initial_symbols):
    s, _ = format_solutions(solution)
    tools = [k for k in TOOL2IDX.keys()]
    response_solution, response_tools, response_symbols = annotate_solutions(s, tools, initial_symbols)
    return response_solution, (response_tools, response_symbols)

