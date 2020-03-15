from collections import Counter, namedtuple
import json
from pathlib import Path

import pandas as pd
import spacy

from analyse import text_import, searching_all_files

nlp = spacy.load('en_core_web_sm')


def word_counter(list_of_articles):
    dict_of_words = {}
    print(list_of_articles)
    for article in list_of_articles:
        text = article["body"]
        text = text.replace(".", " ")
        for word in text.split(" "):
            try:
                dict_of_words[word] += 1
            except KeyError:
                dict_of_words[word] = 1
    dict_of_words = {k: v for k, v in sorted(dict_of_words.items(), key=lambda item: item[1])}
    print(dict_of_words)
    return(dict_of_words)


def word_counter_spacy(article):
    doc = nlp(article['body'])
    return [str(w.lemma_) for w in doc if (not w.is_stop) and (not w.is_punct) and (not w.is_space)]




def save_dict(dictionary, fname='wordlist'):
    path_folder = Path.home() / "climate-nlp" / "{}.csv".format(fname)
    with open(str(path_folder), 'w') as csv_file:
        for word in dictionary:
            csv_file.write(str(word) + ", " + str(dictionary[word]) + "\n")


if __name__ == '__main__':
    list_of_articles = text_import()
    dict_of_wordcounter = word_counter(list_of_articles)
    save_dict(dict_of_wordcounter)

    #  needed for the spacy integration
    filter = [a for a in list_of_articles if a['language'] == 'english']
    corpus = []
    for article in list_of_articles:
        corpus.extend(word_counter_spacy(article))

    c = Counter(corpus)
    corpus = sorted(c.items(), key=lambda x: (x[1], x[0]), reverse=False)

    df = pd.DataFrame(corpus)
    df.columns = ['token', 'count']
    df.to_csv(Path.home() / 'climate-nlp' / 'spacy-counts.csv')
