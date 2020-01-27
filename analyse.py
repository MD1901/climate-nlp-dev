import argparse
from collections import defaultdict
import json
import operator
from pathlib import Path

from polarity_analyser import Polarity

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


def text_import(id=""):
    if not id == "":
        local_list_articles = []
        path_folder = Path.home() / "climate-nlp" / "articles"
        for file_path in searching_all_files(path_folder):
            if id in str(file_path):
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                    local_list_articles.append(data)
        return local_list_articles

    else:
        local_list_articles = []
        path_folder = Path.home() / "climate-nlp" / "articles"
        for file_path in searching_all_files(path_folder):
            print("Importing text from: " + file_path)
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                local_list_articles.append(data)
        return local_list_articles


def save_list(pol_list):
    file_path = Path.home() / "climate-nlp" / "polarity_list.csv"

    with open(file_path, "w") as file:
        file.write("id, polarity_value")
        for id in pol_list:
            file.write(str(id) + "; " + str(pol_list[id]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', default="", nargs='?')
    args = parser.parse_args()
    list_articles = text_import(args.id)
    polarity_list = {}
    number_articles = 200
    counter = 0
    model = Polarity("english")
    for article in list_articles:
        polarity_list[article["id"]] = model.analyse(article["body"])
    save_list(polarity_list)
