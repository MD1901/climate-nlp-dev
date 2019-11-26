import requests
from bs4 import BeautifulSoup
from pathlib import Path
import json
import nltk
from nltk.tokenize import RegexpTokenizer #Are those even necessary?
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim import corpora
from gensim.models import LsiModel

def searching_all_files(directory):
    dirpath = Path(directory)
    assert(dirpath.is_dir())
    file_list = []
    for x in dirpath.iterdir():
        if x.is_file():
            file_list.append(x)
        elif x.is_dir():
            file_list.extend(searching_all_files(x))
    return file_list
def text_import():
    path_folder = Path.home() / "climate-nlp"

    for i in searching_all_files(path_folder):
        if ".json" in str(i):
            with open(str(i), 'r') as json_file:
                data = json.load(json_file)

                print('Url: ' + data['url'])
                print('Text: ' + data['body'])
                print('Date: ' + data['date'])
                print('Author: ' + data['author'])
                print('')
                try:
                    print(text_clean(data['body'], data['lang']))
                except KeyError:
                    print(text_clean(data['body']))
def text_clean(text, lang = "english"):
    tokenizer = RegexpTokenizer(r'\w+')
    en_stop = set(stopwords.words(lang))
    tokens = tokenizer.tokenize(text)
    rem_stop = [w for w in tokens if not w in en_stop]
    lemmatizer = WordNetLemmatizer()
    lemat = [lemmatizer.lemmatize(w) for w in rem_stop]
    return lemat


text_import()
