import pickle
import re


def print_text_and_structure(text_dict, query):
    cnt = 0
    for section, section_dict in text_dict.items():
        for id, text_section in section_dict['text'].items():
            if re.search(query, text_section, re.IGNORECASE):
                total_string = [text_section]
                # print text and structure:
                parent_id = section_dict['structure'][id]
                while parent_id != -1:
                    total_string.insert(0, section_dict['text'][parent_id])
                    parent_id = section_dict['structure'][parent_id]
                print(str(cnt) + '.********************\n')
                cnt = cnt + 1
                for k, sub_string in enumerate(total_string):
                    print(''.join(['*'] * (k + 1)) + '   ' + sub_string)
                print('\n')


if __name__ == "__main__":
    with open('docs/Directive_2017_745_5Apr2017.pickle', 'rb') as handle:
        doc_dict = pickle.load(handle)

    QUERY_TEXT = 'case of minors and of incapacitated subjects, an authori'  # Clinical evaluation plan' # 'Clinical development plan'

    print_text_and_structure(doc_dict, QUERY_TEXT)
