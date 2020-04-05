from collections import namedtuple
import json
from pathlib import Path
#import spacy
from spacy_wrapper import load_spacy_wrapper
from newspapers import newspapers as all_newspapers


def word_counter(list_of_articles):
    dict_of_words_en = {}
    dict_of_words_de = {}

    for article in list_of_articles:
        newspaper = get_newspapers(article["newspaper"])[0]
        language = newspaper["language"]

        spacy_nlp = load_spacy_wrapper(language, version='standard')
        text = article["body"]
        doc = spacy_nlp(text)
        tokens = [token for token in doc if not (token.is_stop or token.is_stop or token.is_punct)]
        if language == "german":
            for word in tokens:
                try:
                    dict_of_words_de[word.lemma_] += 1
                except KeyError:
                    dict_of_words_de[word.lemma_] = 1
            dict_of_words_de = {k: v for k, v in sorted(dict_of_words_de.items(), key=lambda item: item[1])}
        else:
            for word in tokens:
                try:
                    dict_of_words_en[word.lemma_] += 1
                except KeyError:
                    dict_of_words_en[word.lemma_] = 1
            dict_of_words_en = {k: v for k, v in sorted(dict_of_words_en.items(), key=lambda item: item[1])}

    print(dict_of_words_de)
    return dict_of_words_de, dict_of_words_en


def searching_all_files(directory):
    dirpath = Path(directory)
    return [a for a in dirpath.glob('**/*.json')]


def save_dict(dictionary, suffix):
    path_folder = Path.home() / "climate-nlp"
    with open(str(path_folder) + "/wordlist" + suffix + ".csv", 'w') as csv_file:
        for word in dictionary:
            csv_file.write(word + ", " + str(dictionary[word]) + "\n")


def text_import():
    print('importing articles')

    articles = []
    path_folder = Path.home() / "climate-nlp" / "interim"
    for file_path in searching_all_files(path_folder):
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            articles.append(data)

    print('imported {} articles'.format(len(articles)))
    return articles

def get_newspapers(newspapers):
    return [n for n in all_newspapers if n['newspaper'] in newspapers]


if __name__ == '__main__':
    articles = text_import()
    # dict_of_wordcounter_de, dict_of_wordcounter_en = word_counter(list_of_articles)
    # print(dict_of_wordcounter_en)
    # save_dict(dict_of_wordcounter_de, "de")
    # save_dict(dict_of_wordcounter_en, "en")

    limit = 10
    for article in articles[:limit]:
        pass

