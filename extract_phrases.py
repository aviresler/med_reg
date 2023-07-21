import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import re

#model = SentenceTransformer('all-mpnet-base-v2')
model = SentenceTransformer('all-MiniLM-L6-v2')


def get_phrases(text_dict, n_words):
    with open('docs/stop_words.txt') as f:
        lines_ = f.readlines()

    stop_words = [word.strip() for word in lines_]

    out = []
    for section, dict_ in text_dict.items():
        for loc, text in dict_['text'].items():
            text = text.replace('\n', ' ')

            words = text.split(' ')
            # removing words with numbers
            words = [word.strip() for word in words if not any(char.isdigit() for char in word)]

            for k in range(len(words)):
                if k + n_words > len(words):
                    break

                phrase_list = words[k:k + n_words]
                # remove phrases with more than 2 stop words
                cnt = 0
                for word in phrase_list:
                    if word in stop_words:
                        cnt = cnt + 1
                if cnt >= 2:
                    continue

                phrase = ' '.join(phrase_list)
                out.append(phrase.lower().strip())

    result = []
    # remove duplicates
    [result.append(x) for x in out if x not in result]
    return result


def save_phrases_and_embeddings(file):
    with open(file, 'rb') as handle:
        doc_dict = pickle.load(handle)

    phrases_2 = get_phrases(doc_dict, 2)
    phrases_3 = get_phrases(doc_dict, 3)
    phrases_4 = get_phrases(doc_dict, 4)

    phrases_ = phrases_2 + phrases_3 + phrases_4

    embeddings = model.encode(phrases_, show_progress_bar=True, batch_size=128)

    with open('docs/phrases.txt', 'w') as fp:
        for item in phrases_:
            # write each item on a new line
            fp.write(item+"\n")

    np.save('docs/phrases_embed.npy', embeddings)


if __name__ == "__main__":
    #save_phrases_and_embeddings('docs/Directive_2017_745_5Apr2017.pickle')

    # load embeddings
    embed = np.load('docs/phrases_embed.npy')

    with open('docs/phrases.txt') as f:
        lines = f.readlines()

    phrases = [line.strip('\n') for line in lines]

    QUERY = 'Clinical evaluation plan'
    query_embed = model.encode(QUERY, show_progress_bar=True, batch_size=128)
    query_embed = np.expand_dims(query_embed, axis=0)
    similarity = cosine_similarity(embed, query_embed)
    similarity = np.squeeze(similarity)
    most_similar_inds = np.argsort(-similarity)

    N_similar_phrases = 100
    most_similar_inds = most_similar_inds[:N_similar_phrases]
    already_printed = []
    for k in range(N_similar_phrases):
        ind = most_similar_inds[k]
        candidate = phrases[ind]
        already_printed.append(candidate)
        print('{0}    sim={1:.2f}'.format(candidate, similarity[ind]))
