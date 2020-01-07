from collections import defaultdict
import json
import operator
from pathlib import Path

from polarity_analyser import Polarity_with_shifter

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
    path_folder = Path.home() / "climate-nlp" / "articles"
    for file_path in searching_all_files(path_folder):
        print("Importing text from: " + file_path)
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            local_list_articles.append(data)
    return local_list_articles


def save_list(pol_list):
    file_path = Path.home() / "climate-nlp" / "polarity_list.csv"
    result = ""
    for id in pol_list:
         result += str(id) + ", " + str(pol_list[id]) + "\n"

    with open(file_path, "w") as file:
        file.write(result)



if __name__ == '__main__':
    list_articles = text_import()
    polarity_list = {}
    number_articles = 200
    counter = 0
    model = Polarity_with_shifter("english")
    for article in list_articles:
        polarity_list[article["id"]] = model.analyse(article["body"])
    save_list(polarity_list)
