

import re
import numpy as np
import pickle

# @todo: improve structure

REGULATION_FILE = 'docs/Directive_2017_745_5Apr2017_2.txt'
with open(REGULATION_FILE, 'r', encoding="utf-8") as f:
    full_text = f.read()

# intro_text ends in first occurrence of 'CHAPTER I'
intro_loc = re.search('CHAPTER I', full_text)
intro_text = full_text[:intro_loc.regs[0][0]]
# main_text  ends in first occurrence of 'ANNEXES'
# annexes_text - the rest of the document
annexes_loc = re.search('ANNEXES', full_text)
annexes_text = full_text[annexes_loc.regs[0][0]:]
main_text = full_text[intro_loc.regs[0][0]:annexes_loc.regs[0][0]]

reg_exps_introduction =[
    '\n\((\d+)\) ']

reg_exps_main_text =[
    '(CHAPTER .*)\n\n?(.*)',
    '\n(Article \d*)\n\n?(.*)',
    '\n(\d*)\. ',
    '\n\d+\.\d+\.? ',
    '\n\d+\.\d+\.\d+\.? ',
    '\n\([a-z]\)',
    '\n ']

reg_exps_annexes =[
    '(ANNEX .*)\n\n?(.*)',
    '(CHAPTER .*)\n\n?(.*)',
    '(PART .*)\n\n?(.*)', # there won't always be part under each annex
    '\n(\d*)\. ',
    '\n\d+\.\d+\.? ',
    '\n\d+\.\d+\.\d+\.? ',
    '\n\([a-z]\)',
    '\n ']

def parse_text(text, reg_exps, prefix):
    mask = np.zeros(len(text),dtype=int)
    for k, regexp in enumerate(reg_exps):
        # find locations in text
        p = re.compile(regexp)
        for m in p.finditer(text):
            mask[m.start()] = k + 1

    # gather text sections
    out_text = {}
    out_struct = {}
    borders = np.nonzero(mask)[0]
    for i in range(borders.size - 1):
        start = borders[i]
        end = borders[i+1]
        id = prefix + '_' + str(start)
        out_text[id] = text[start:end].strip()

        # find parent, by searching to the previous closest level in the mask
        my_level = mask[borders[i]]
        parent_level = my_level - 1
        if parent_level > 0:
            parent_loc = np.where((mask[:start] > 0) & (mask[:start] < my_level) )[0][-1]
            parent_id = prefix + '_' + str(parent_loc)
            out_struct[id] = parent_id
        else:
            out_struct[id] = -1

    out = {'text': out_text, 'structure': out_struct}
    return out


dict_intro = parse_text(intro_text, reg_exps_introduction, 'intro')
dict_main = parse_text(main_text, reg_exps_main_text, 'main')
dict_annexes = parse_text(annexes_text, reg_exps_annexes,'annex')

save_dict = {'intro': dict_intro, 'main': dict_main, 'annexes': dict_annexes}

with open('Directive_2017_745_5Apr2017.pickle', 'wb') as handle:
    pickle.dump(save_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
