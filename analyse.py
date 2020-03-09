import argparse
from collections import defaultdict
import json
import operator
from pathlib import Path

import pandas as pd

from models import AdamSimple
from polarity_analyser import Polarity

# do we need a word class? is_neg, intensity
# norm by count, maybe scale by frequency
# https://www.youtube.com/watch?v=By4IZeIzxIw min 9:30
# count num pos versus num neg

HOME = Path.home() / "climate-nlp"


def searching_all_files(directory):
    print('searching_all_files {}'.format(directory))
    dirpath = Path(directory)
    assert dirpath.is_dir()
    file_list = []
    # for dir_path in dirpath.iterdir():
    #     print("Importing files from: " + str(dir_path))
    #     if dir_path.is_dir():
    for file_path in dirpath.iterdir():
        if file_path.is_file():
            if ".json" in str(file_path):
                file_list.append(str(file_path))
    return file_list


def text_import(doc_id=""):
    if not doc_id == "":
        local_list_articles = []
        path_folder = Path.home() / "climate-nlp" / "interim"
        for file_path in searching_all_files(path_folder):
            if doc_id in str(file_path):
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                    local_list_articles.append(data)
        return local_list_articles

    else:
        local_list_articles = []
        path_folder = Path.home() / "climate-nlp" / "interim"
        for file_path in searching_all_files(path_folder):
            print("Importing text from: " + file_path)
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                local_list_articles.append(data)
        return local_list_articles


def save_list(pol_list):
    file_path = Path.home() / "climate-nlp" / "polarity_list.csv"

    with open(file_path, "w") as fi:
        fi.write("id, polarity_value")
        for doc_id in pol_list:
            fi.write(str(doc_id) + "; " + str(pol_list[doc_id]))


def find_doc(doc_id, polarity_list):
    for doc in polarity_list:
        if doc['id']:
            if doc['id'][:len(doc_id)] == doc_id:
                return doc
    return None


def add_document_statistics(doc):
    doc['polarities'] = [res[1] for res in doc['result']]
    doc['sum'] = sum(doc['polarities']) / len(doc['polarities'])
    doc['newspaper'] = doc['url'].split('/')[2]
    return doc


def split_and_save_html(doc_id, polarity_list):
    doc = find_doc(doc_id, polarity_list)
    # split into sentences
    sentences = []
    sentence = []
    for word, polarity in doc['result']:
        sentence.append((word, polarity))
        if word:
            if word[-1] == '.':
                sentences.append(sentence)
                sentence = []

    out_dir = HOME / 'final'
    out_dir.mkdir(parents=True, exist_ok=True)
    save_html(
        doc,
        sentences,
        out_file=out_dir / '{}.html'.format(doc_id)
    )


def save_html(doc, sentences, out_file):
    document, tag, text = Doc().tagtext()

    with tag('html'):
        with tag('body'):
            with tag('p'):
                text('sum {} wc {} {}'.format(
                    doc['sum'],
                    len(doc['polarities']),
                    doc['url']
                ))

            # for word, polarity in result:
            for sentence in sentences:
                with tag('p'):

                    for word, polarity in sentence:

                        clr = '#000000'
                        if polarity > 0:
                            clr = '#00cc00'
                            word += ' ({})'.format(polarity)
                        elif polarity < 0:
                            clr = '#ff0000'
                            word += ' ({})'.format(polarity)
                        with tag('span', style="color: {}".format(clr)):
                            text(word + ' ')

    result = document.getvalue()

    with open(out_file, 'w') as fi:
        fi.write(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_id', default='simple-sentence', nargs='?')
    parser.add_argument('--id', default="", nargs='?')
    args = parser.parse_args()
    polarity_dict = pd.read_csv('./lexica/english/polarity.txt')

    new = {}
    for row in range(polarity_dict.shape[0]):
        try:
            new[polarity_dict.iloc[row, 0]] = int(polarity_dict.iloc[row, 1])
        except:
            pass

    polarity_dict = new
    models = {
        # 'polarity-shifter': Polarity_with_shifter("english"),
        'simple-sentence': AdamSimple(polarity_dict),
        'basic': Polarity("english"),
    }
    links = text_import(args.id)
    import pdb; pdb.set_trace()

    link = links[-1]
    print(link['url'])

    avoids = ['zfd6n39', ]
    for avoid in avoids:
        links = [l for l in links if avoid not in l['url']]

    polarity_list = []
    model = models[args.model_id]
    list_articles = links
    for article in list_articles:
        # polarity_list[["id"]] = sum))
        body = article["body"]
        result = model.analyse(body)
        polarity_list.append(
            {
                'url': article['url'],
                'id': article["id"],
                'clean-id': article['id'].split('?')[0],
                'body': body,
                "result": result,
            }
        )

    doc_id = 'what-will-another-decade-of-climate-crisis-bring'
    doc = find_doc(doc_id, polarity_list)
    #  save to disk
    docs = [add_document_statistics(doc) for doc in polarity_list]

    # break here between model and analyse TODO

    import matplotlib.pyplot as plt

    corpus_polarities = []
    for doc in docs:
        corpus_polarities.extend(doc['polarities'])

    f, a = plt.subplots()
    a.hist(corpus_polarities)
    f.savefig('word-polarities.png')

    df = pd.DataFrame(docs)
    df.drop(['id', 'body', 'result' , 'polarities', 'url'], inplace=True, axis=1)

    f, a = plt.subplots()
    a.hist(df.loc[:, 'sum'])
    f.savefig('doc-polarities.png')

    # groupby newspaper
    papers = df.groupby('newspaper').mean()

    print(df.sort_values('sum').head(10))
    print(' ')
    print(df.sort_values('sum', ascending=False).head(10))
    print(papers)
    from yattag import Doc

    for doc_id in df.loc[:, 'clean-id'].values:
        split_and_save_html(doc_id, polarity_list)
