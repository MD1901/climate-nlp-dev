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


def open_html(newspapers):
    text = ""
    date = ""
    author = ""
    data_html = Path.home() / "climate-nlp" / "raw"
    newspaper_parsers = {
        "theguardian.com": parse_guardian
    }
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
                    if news.name == newspaper:
                        lang = news.language
                        print(lang)
                json_filepath = str(file_path).replace(".html",".json")
                url = ""
                id = str(file_path).split("/")[-1].replace(".html", "")
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
if __name__ == '__main__':
    newspapers = import_newspapers()
    open_html(newspapers)
