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

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_id', default='polarity-shifter', nargs='?')
    # parser.add_argument('--log_every', default=100, nargs='?')
    # parser.add_argument('--save_every', default=1000, nargs='?')
    # parser.add_argument('--epochs', default=10, nargs='?')
    # parser.add_argument('--data', default='local', nargs='?')
    # parser.add_argument('--dataset', default='random-rollouts', nargs='?')
    args = parser.parse_args()

    from test_polarity import ModelWrapper

    import pandas as pd
    polarity_dict = pd.read_csv('./data/polarity.txt')

    new = {}
    for row in range(polarity_dict.shape[0]):
        try:
            new[polarity_dict.iloc[row, 0]] = int(polarity_dict.iloc[row, 1])
        except:
            pass

    polarity_dict = new
    models = {
        # 'polarity-shifter': Polarity_with_shifter("english"),
        'simple-sentence': ModelWrapper(polarity_dict)
    }

    list_articles = text_import()
    polarity_list = []
    number_articles = 200
    counter = 0
    model = models[args.model_id]
    for article in list_articles:
        # polarity_list[["id"]] = sum))

        polarity_list.append(
            {'id': article["id"], "sum": model.analyse(article["body"])}
        )

    polarity_list = pd.DataFrame(polarity_list)

    # save_list(polarity_list)

