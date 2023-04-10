
import pickle
import re

with open('docs/Directive_2017_745_5Apr2017.pickle', 'rb') as handle:
    doc_dict = pickle.load(handle)

QUERY_TEXT = 'Clinical evaluation plan' # 'Clinical development plan'

cnt  = 0
for section, section_dict in doc_dict.items():
    for id, text_section in section_dict['text'].items():
        if re.search(QUERY_TEXT, text_section, re.IGNORECASE):
            total_string = []
            total_string.append(text_section)
            # print text and structure:
            parent_id = section_dict['structure'][id]
            while parent_id != -1:
                total_string.insert(0, section_dict['text'][parent_id])
                parent_id = section_dict['structure'][parent_id]
            print(str(cnt) + '.********************\n')
            cnt = cnt + 1
            for k, sub_string in enumerate(total_string):
                print(''.join(['*']*(k+1)) + '   ' + sub_string)
            print('\n')

