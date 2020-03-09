from collections import namedtuple
import json
from pathlib import Path

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


def searching_all_files(directory):
    dirpath = Path(directory)
    return [a for a in dirpath.glob('**/*.json')]


def save_dict(dictionary):
    path_folder = Path.home() / "climate-nlp"
    with open(str(path_folder) + "/wordlist.csv", 'w') as csv_file:
        for word in dictionary:
            csv_file.write(word + ", " + str(dictionary[word]) + "\n")


def text_import():
    local_list_articles = []
    path_folder = Path.home() / "climate-nlp" / "interim"
    for file_path in searching_all_files(path_folder):
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            local_list_articles.append(data)
    return local_list_articles


if __name__ == '__main__':
    list_of_articles = text_import()
    dict_of_wordcounter = word_counter(list_of_articles)
    save_dict(dict_of_wordcounter)
