import os
import json
import errno
import re
from .constants import BASE_PAGE, SAVE_PATH_OF_SOLVABLE_LEVELS


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def clean_level_pack_links(set_of_results):
    final_links = []
    for f in set_of_results:
        if len(f) == 0 or len(f) > 1:
            continue
        final_links.append(BASE_PAGE + f[0]['href'])
    return final_links


def clean_level_pack_level_links(set_of_results):
    final_links = []
    for f in set_of_results:
        if len(f) == 0:
            continue
        elif len(f) > 1:
            f = [f[-1]]
        print(f[0].text)
        if 'Mobile' in f[0].text:
            continue
        final_links.append(BASE_PAGE + f[0]['href'])
    return final_links


def post_process_func_pack_scraper(soup):
    content = soup.find("table")
    possible_content_links = [f.find_all(name='a') for f in content.find_all(name='th')]
    result_obj = clean_level_pack_links(possible_content_links)
    return result_obj


def post_process_func_pack_solvable_identifier(level_name, solvable_levels, soup):
    content = soup.find('table', {'class': 'article-table'})
    possible_content_links = [f.find_all('a') for f in content.find_all('td')]
    clean_possible_links = clean_level_pack_level_links(possible_content_links)
    if len(clean_possible_links) > 0:
        solvable_levels.update({level_name: clean_possible_links})
    return solvable_levels


def get_symbols(text):
    # Define a regular expression to match single or double capital letter words
    pattern = r'\b[A-Z]{1,4}\b'

    # Find matches in the text using the regular expression and store their positions
    matches = [(match.group(), match.start()) for match in re.finditer(pattern, text)]

    # Sort the matches based on their positions in the text
    sorted_matches = sorted(matches, key=lambda x: x[1])

    # Extract the matched elements and return them in order
    elements = [match[0] for match in sorted_matches]

    return elements


def compare_symbols(history, new):
    unique_elements = set(new) - set(history)
    return list(unique_elements)



def enumerate_solvable_levels():
    """
    Run this once to convert entries of solvable_levels.json from list, to list of tuples
    """
    if os.path.exists(SAVE_PATH_OF_SOLVABLE_LEVELS):
        with open(SAVE_PATH_OF_SOLVABLE_LEVELS, 'r') as fin:
            data = json.load(fin)

        for k, v in data.items():
            if isinstance(v, list):
                if isinstance(v[0], str):
                    print("File is in format List[urls]...converting")
                    convert_flag = True
                    break
                else:
                    print("File is in format List[Tuple(int,url)]...all good")
                    convert_flag = False
                    break
            else:
                print("File is not correct, please re-run pack_scraper.py!")

        if convert_flag:
            new_data = {}
            for k, v in data.items():
                new_data.update({k: [(i, v) for i, v in enumerate(v)]})
            with open('test.json', 'w') as fout:
                json.dump(new_data, fout)
    return



