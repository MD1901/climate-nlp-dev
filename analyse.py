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
    # do we need a word class? is_neg, intensity
    # norm by count, maybe scale by frequency
    # https://www.youtube.com/watch?v=By4IZeIzxIw min 9:30
    # count num pos versus num neg

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_id', default='polarity-shifter', nargs='?')
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
    counter = 0
    model = models[args.model_id]
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
    doc = [doc for doc in polarity_list
           if doc['id'][:len(doc_id)] == doc_id][0]

    def add_document_statistics(doc):
        doc['polarities'] = [res[1] for res in doc['result']]
        doc['sum'] = sum(doc['polarities'])
        doc['newspaper'] = doc['url'].split('/')[2]
        return doc

    docs = [add_document_statistics(doc) for doc in polarity_list]

    import matplotlib.pyplot as plt

    corpus_polarities = []
    for doc in docs:
        corpus_polarities.extend(doc['polarities'])

    f, a = plt.subplots()
    a.hist(corpus_polarities)
    f.savefig('word-polarities.png')

    df = pd.DataFrame(docs)
    df.drop(['body', 'result' , 'polarities'], inplace=True, axis=1)
    print(df.sort_values('sum').head(10))
    print(df.sort_values('sum', ascending=False).head(10))

    f, a = plt.subplots()
    a.hist(df.loc[:, 'sum'])
    f.savefig('doc-polarities.png')

    # groupby newspaper
    papers = df.groupby('newspaper').mean()
    print(papers)
    from yattag import Doc

    def save_html(sentences):
        doc, tag, text = Doc().tagtext()

        with tag('html'):
            with tag('body'):

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

        result = doc.getvalue()

        with open('out.html', 'w') as fi:
            fi.write(result)

    #  class Word TODO

    # split into sentences
    sentences = []
    sentence = []
    for word, polarity in doc['result']:
        sentence.append((word, polarity))
        if word:
            if word[-1] == '.':
                sentences.append(sentence)
                sentence = []

    save_html(sentences)


