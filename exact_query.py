import pickle
import re


# equal branch is a branch where all elements but the last one are identical
def get_equal_branches(candidates):
    branch_list = []
    for candidate in candidates:
        branch = ''.join(candidate[:-1])
        branch_list.append(branch)
    unique_branches = set(branch_list)
    out = []
    for branch in unique_branches:
        indices_branch = [i for i, x in enumerate(branch_list) if x == branch]
        if len(indices_branch) > 1:
            out.append(indices_branch)

    return out


def print_candidate(list_of_strings, index):
    print(str(index) + '.********************\n')
    for k, sub_string in enumerate(list_of_strings):
        print(''.join(['*'] * (k + 1)) + '   ' + sub_string)
    print('\n')


def print_text_and_structure(text_dict, query):
    # collect potential candidates that should be printed
    candidates = []
    for section, section_dict in text_dict.items():
        for id_, text_section in section_dict['text'].items():
            # search for query in the text
            if re.search(query, text_section, re.IGNORECASE):
                total_string = [text_section]
                # collect text and structure:
                parent_id = section_dict['structure'][id_]
                while parent_id != -1:
                    total_string.insert(0, section_dict['text'][parent_id])
                    parent_id = section_dict['structure'][parent_id]
                total_string.insert(0,section)
                candidates.append(total_string)

    # equal branches are branches where all elements but the last one are identical
    equal_branches = get_equal_branches(candidates)
    equal_branches_list = []
    already_taken_care_of = []
    for branches in equal_branches:
        total_string_eb = candidates[branches[0]][:-1]
        suffix = ''
        for element in branches:
            already_taken_care_of.append(element)
            suffix += candidates[element][-1] + '\n'
        total_string_eb += [suffix.strip()]
        equal_branches_list.append(total_string_eb)

    cnt = 0
    # print equal branches
    for eb in equal_branches_list:
        print_candidate(eb, cnt)
        cnt += 1

    for c, candidate in enumerate(candidates):
        if c in already_taken_care_of:
            continue
        else:
            print_candidate(candidate, cnt)
            cnt += 1


if __name__ == "__main__":
    with open('docs/Directive_2017_745_5Apr2017.pickle', 'rb') as handle:
        doc_dict = pickle.load(handle)

    QUERY_TEXT = 'Clinical evaluation plan'  # Clinical evaluation plan' # 'Clinical development plan'

    print_text_and_structure(doc_dict, QUERY_TEXT)
