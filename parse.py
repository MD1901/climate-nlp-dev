import argparse
from collections import namedtuple
import json
from pathlib import Path
import requests

from bs4 import BeautifulSoup

from download import import_newspapers


def searching_all_files(directory):
    dirpath = Path(directory)
    assert dirpath.is_dir()
    file_list = []
    for dir_path in dirpath.iterdir():
        if dir_path.is_dir():
            for file_path in dir_path.iterdir():
                if file_path.is_file():
                    if ".html" in str(file_path):
                        file_list.append(str(file_path))
    return file_list


def searching_all_files(directory):
    dirpath = Path(directory)
    return [a for a in dirpath.glob('**/*.html')]


def parse_guardian(soup):
    text = ""
    date = ""
    author = ""
    for paragraph in soup.find_all("p"):
        try:
            paragraph["class"]
        except KeyError:
            text += paragraph.text + " "
    for time_tag in soup.find_all("time"):
        try:
            date = time_tag["datetime"]
            break
        except KeyError:
            break
    return text, author, date


def parse_fox(soup):
    text = ""
    date = ""
    author = ""
    for paragraph in soup.find_all("p"):
        # if paragraph.find_par
        parents = [p for p in paragraph.find_parents()]
        import pdb; pdb.set_trace()
        text += paragraph.text + " "

    for time_tag in soup.find_all("time"):
        try:
            date = time_tag["datetime"]
            break
        except KeyError:
            break
    return text, author, date


def parse_standard(soup):
    text = ""
    date = ""
    author = ""
    for paragraph in soup.find_all("p"):
        text += paragraph.text + " "

    for time_tag in soup.find_all("time"):
        try:
            date = time_tag["datetime"]
            break
        except KeyError:
            break
    return text, author, date

newspaper_parsers = {
    "theguardian": parse_guardian,
    "foxnews": parse_fox
}

def open_html(newspapers):
    text = ""
    date = ""
    author = ""
    data_html = Path.home() / "climate-nlp" / "raw"
    list_of_files = searching_all_files(data_html)
    for file_path in list_of_files:
        if ".html" in str(file_path):
            print(str(file_path))
            with open(file_path, 'r') as html_file:
                soup = BeautifulSoup(html_file, features="html.parser")
                newspaper = str(file_path).split("/")[5].replace("_", ".")
                try:
                    soup_parser = newspaper_parsers[newspaper]
                    text, author, date = soup_parser(soup)

                except KeyError:
                    text, author, date = parse_standard(soup)
                data_home = Path.home() / "climate-nlp" / "articles" /  newspaper.replace(".", "_")
                data_home.mkdir(parents=True, exist_ok=True)
                lang = "english"
                for news in newspapers:
                    if news.url == newspaper:
                        lang = news.language
                        print(lang)
                json_filepath = str(file_path).replace(".html",".json")
                url = ""
                id = str(file_path).split("/")[-1].replace(".html", "")
                try:
                    with open(json_filepath, 'r') as json_file:
                        data = json.load(json_file)
                        url = data["url"]
                    result = {
                        "id": id,
                        "url": url,
                        "body": text,
                        "date": date,
                        "author": author,
                        "lang": lang
                    }
                    print(result)
                    filename = str(file_path).replace(".html",".json").replace("raw", "articles")
                    with open(filename, 'w') as fp:
                        json.dump(result, fp)
                except FileNotFoundError:
                    pass


def open_html(newspapers):
    newspapers = [n.url.split('.')[0] for n in newspapers]

    all_files = searching_all_files(Path.home() / "climate-nlp" / "raw")

    for fi in all_files:

        #  function
        for paper in newspapers:
            print(paper)
            print(str(fi))
            if paper in str(fi):
                print(fi)
                parser = newspaper_parsers.get(paper, parse_standard)

                with open(fi, 'r') as html:
                    html = BeautifulSoup(html, features="html.parser")
                with open(fi.with_suffix('.json'), 'r') as json_f:
                    json_f = json.load(json_f)

                data_home = Path.home() / "climate-nlp" / "articles" / paper
                text, author, date = parser(html)
                result = {
                    "id": str(fi).split('/')[-1].replace(".html", "").split('?')[0],
                    "url": json_f['url'],
                    "body": text,
                    "date": date,
                    "author": author,
                }
                out_fi = str(fi).replace(".html",".json").replace("raw", "articles")
                with open(out_fi, 'w') as fp:
                    json.dump(result, fp)

if __name__ == '__main__':
    newspapers = import_newspapers('fox')
    print(newspapers)
    open_html(newspapers)
