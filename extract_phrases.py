import pickle


def get_phrases(text_dict, n_words):
    out = []
    for section, dict_ in text_dict.items():
        for loc, text in dict_['text'].items():
            words = text.split(' ')
            # removing words with numbers
            words = [word for word in words if not any(char.isdigit() for char in word)]
            # consider removing phrases with more than 2 stop words
            
            for k in range(len(words)):
                if k+n_words > len(words):
                    break
                phrase = ' '.join(words[k:k+n_words])
                out.append(phrase)

    return out


if __name__ == "__main__":
    with open('docs/Directive_2017_745_5Apr2017.pickle', 'rb') as handle:
        doc_dict = pickle.load(handle)

    #phrases_2 = get_phrases(doc_dict, 2)
    phrases_3 = get_phrases(doc_dict, 3)
    phrases_4 = get_phrases(doc_dict, 4)
    print('bb')
