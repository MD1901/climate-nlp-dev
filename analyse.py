from pathlib import Path
import json
import operator
from nltk.tokenize import RegexpTokenizer #Are those even necessary?
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def searching_all_files(directory):
    # NEU! Nicht rekursiv sondern: Zeitungen importieren und dann nur bis append.

    dirpath = Path(directory)
    assert dirpath.is_dir()
    file_list = []
    for file in dirpath.iterdir():
        if file.is_file():
            file_list.append(file)
        elif file.is_dir():
            file_list.extend(searching_all_files(file))
    return file_list

def text_import():
    list_articles = []
    path_folder = Path.home() / "climate-nlp"
    for i in searching_all_files(path_folder):
        if ".json" in str(i):
            with open(str(i), 'r') as json_file:
                data = json.load(json_file)
                try:
                    data['clean'] = text_clean(data['body'], data['lang'])
                except KeyError:
                    data['clean'] = text_clean(data['body'])
                list_articles.append(data)
    return list_articles

def text_clean(text, lang="english"):
    tokenizer = RegexpTokenizer(r'\w+')
    en_stop = set(stopwords.words(lang))
    tokens = tokenizer.tokenize(text)
    rem_stop = [w for w in tokens if not w in en_stop]
    lemmatizer = WordNetLemmatizer()
    lemat = [lemmatizer.lemmatize(w) for w in rem_stop]
    return lemat

def dict_import(lang):
    dict = {}
    if lang == "german" or lang == "english":
        with open(lang + "_wordlist.txt", "r") as f:
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
        if word in dict:
            sum += int(dict[word])
    if len(text): polarity_value = sum / len(text)
    return polarity_value

if __name__ == '__main__':
    list_articles = text_import()
    polarity_list = {}
    for article in list_articles:
        polarity_list[article["url"]] = polarity(article["clean"], article["lang"])

    best_polarity = max(polarity_list.items(), key=operator.itemgetter(1))
    best_article = ""
    for article in list_articles:
        if article["url"] == best_polarity[0]:
            best_article = article["body"]
    print("Most positive article: \n Value: " + str(best_polarity[1]) + "\n Url: " + best_polarity[0] + "\n Text: " + best_article)
