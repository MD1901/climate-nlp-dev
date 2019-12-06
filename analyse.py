from pathlib import Path
import json
import operator
from nltk.tokenize import RegexpTokenizer #Are those even necessary?
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy


def searching_all_files(directory):
    dirpath = Path(directory)
    assert dirpath.is_dir()
    file_list = []
    for dir in dirpath.iterdir():
        print("Importing files from: " + str(dir))
        if dir.is_dir():
            for file in dir.iterdir():
                if file.is_file():
                    file_list.append(str(file))
    return file_list


def text_import():
    models = {german = spacy.load("de_core_news_sm")
    english = spacy.load("en_core_web_sm")}

    list_articles = []
    path_folder = Path.home() / "climate-nlp"
    for i in searching_all_files(path_folder):
        if ".json" in str(i):
            print("Importing text from: " + str(i))
            with open(str(i), 'r') as json_file:
                data = json.load(json_file)
                try:
                    if data['lang'] == "german":
                        data['doc'] = german(data['body'])
                    else:
                        data['doc'] = english(data['body'])
                except KeyError:
                    data['doc'] = english(data['body'])
                list_articles.append(data)
    return list_articles

def dict_import(lang):
    dict = {}
    if lang == "german" or lang == "english":
        with open(lang + "_wordlist.txt", "r") as f:
            #  dict comprehension
            # mydict = {key: value for something in something}
            # mylist = [item for item in something]
            for line in f:
                word, value = line.split("\t")
                dict[word] = value
    else:
        return null

    return dict

def polarity(text, lang):
    to_be_analysed = []
    sum = 0
    dict = dict_import(lang)
    polarity_value = 0
    for word in text:
        if word.text in dict:
            sum += int(dict[word.text])
    if len(text): polarity_value = sum / len(text)
    return polarity_value

if __name__ == '__main__':
    list_articles = text_import()
    polarity_list = {}
    real_entities = set()
    thunberg_counter = 0
    number_articles = 0
    merkel_counter = 0
    trump_counter = 0

    from collections import defaultdict

    counter = defaultdict(int)
    for article in list_articles:
        polarity_list[article["url"]] = polarity(article["doc"], article["lang"])
        number_articles += 1
        for ent in article["doc"].ents:
            real_entities.add(ent)
            if "thunberg" in ent.text.lower():
                thunberg_counter += 1
            if "merkel" in ent.text.lower():
                merkel_counter += 1
            if "trump" in ent.text.lower():
                trump_counter += 1

    print("Number of articles analysed: " + str(number_articles))
    print("Number of mentions of Greta Thunberg: " + str(thunberg_counter))
    print("Number of mentions of Angela Merkel: " + str(merkel_counter))
    print("Number of mentions of Donald Trump: " + str(trump_counter))

    best_polarity = min(polarity_list.items(), key=operator.itemgetter(1))
    best_article = ""
    for article in list_articles:
        if article["url"] == best_polarity[0]:
            best_article = article["body"]
    print("Most negative article: \n Value: " + str(best_polarity[1]) + "\n Url: " + best_polarity[0] + "\n Text: " + best_article)
