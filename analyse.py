from collections import defaultdict
import json
import operator
from pathlib import Path

import spacy

def searching_all_files(directory):
    dirpath = Path(directory)
    assert dirpath.is_dir()
    file_list = []
    for dir_path in dirpath.iterdir():
        print("Importing files from: " + str(dir_path))
        if dir_path.is_dir():
            for file_path in dir_path.iterdir():
                if file_path.is_file():
                    if ".json" in str(file_path):
                        file_list.append(str(file_path))
    return file_list


def text_import():
    local_list_articles = []
    path_folder = Path.home() / "climate-nlp" / "Articles" 
    for file_path in searching_all_files(path_folder):
        print("Importing text from: " + file_path)
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            local_list_articles.append(data)
    return local_list_articles


def dict_import(lang):
    polarity_dict = {}
    if lang in "german english":
        with open(lang + "_wordlist.txt", "r") as open_file:
            for line in open_file:
                word, value = line.split("\t")
                polarity_dict[word] = value
    else:
        return None

    return polarity_dict

def shifter_import():
    shifter_dict = {}
    with open("shifter_lemma_lexicon.csv", "r") as open_file:
        for line in open_file:
                word, value = line.replace("\n", " ").split(",")
                shifter_dict[word] = value
    return shifter_dict

def sentence_polarity(sentence):
    polarity_dict = dict_import("english")
    shifter_dict = shifter_import()
    polarity_sum = 0.0
    words_pol = {}
    words_shift = {}
    for word in sentence:
        if word.lemma_ in polarity_dict:
            words_pol[word] = float(polarity_dict[word.lemma_])
        else:
            words_pol[word] = 0.0
        if word.lemma_ in shifter_dict:
            words_shift[word] = shifter_dict[word.lemma_]
        else:
            words_shift[word] = "nonshifter"

    for word in reversed(sentence):
        if word.dep_ == "neg":
            polarity_sum = -0.7 * polarity_sum
        elif words_shift[word] == "shifter":
            if words_pol[word] == 0:
                polarity_sum = -0.5 * polarity_sum
            else:
                polarity_sum = -0.5 * polarity_sum + words_pol[word]
        elif word.dep_ == "dobj" or word.dep_ == "nsubj":
            polarity_sum += 2*words_pol[word]
        else:
            polarity_sum += float(words_pol[word])
    if not len(sentence) == 0:
        polarity_value = polarity_sum / len(sentence)
    else:
        polarity_value = 0
    return polarity_value


def polarity(text, lang): 
    polarity_sum = 0.0
    if lang == "english":
        model = spacy.load("en_core_web_sm")
    else:
        model = spacy.load("de_core_news_sm")
    text_modeled = model(text)
    for sentence in text_modeled.sents:
        polarity_sum += sentence_polarity(sentence)
    print(str(polarity_sum) + ": " + text)
    return polarity_sum


if __name__ == '__main__':
    list_articles = text_import()
    polarity_list = {}
    number_articles = 200
    counter = 0
    for article in list_articles:
        if counter >= number_articles :
            break
        polarity_list[article["url"]] = polarity(article["body"], article["lang"])
        counter += 1

    best_polarity = min(polarity_list.items(), key=operator.itemgetter(1))
    best_article = ""
    for article in list_articles:
        if article["url"] == best_polarity[0]:
            best_article = article["body"]
            polarity(article["body"], article["lang"])
    print("Most negative article: \n Value: " + str(best_polarity[1]) +
          "\n Url: " + best_polarity[0] + "\n Text: " + best_article)
