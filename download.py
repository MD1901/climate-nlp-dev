import argparse
from collections import namedtuple
import json
from pathlib import Path
import requests

from bs4 import BeautifulSoup
from googlesearch import search

def web_scraper(newspaper, num_results=100):
    """ returns links from a given newspaper """
    queries = {
        "german": "Klimawandel site:",
        "english": "Climate Change site:"
    }
    website, lang = newspaper
    query = queries[lang] + website
    links = [j for j in search(query, tld="co.in", num=num_results, start=1, stop=100)]
    return links


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


def save_html(article):
    newspaper = article[0]
    url = article[1]
    lang = article[2]
    response = requests.get(url)
    data_home = Path.home() / "climate-nlp" / "raw" /  newspaper.replace(".", "_")
    data_home.mkdir(parents=True, exist_ok=True)
    filename = url.replace(".", "").replace(":", "").replace("/", "").replace("@", "") + ".html"
    with open(data_home / filename, 'w') as fp:
        fp.write(response.text)


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
            result = {
                "url": str(file_path),
                "body": text,
                "date": date,
                "author": author,
                "lang": lang
            }
            print(result)
            filename = str(file_path).replace(".html",".json").replace("raw", "articles")
            with open(filename, 'w') as fp:
                json.dump(result, fp)


def main(language, news, onlyopen = False):
    if not onlyopen:
        websites = []
        for new in news:
            if new.language == language:
                links = web_scraper(new)

                for link in links:
                    websites.append((new.url, link, new.language))
                    print(websites[-1])
                    save_html(websites[-1])
        open_html(news)
    else:
        open_html(news)


if __name__ == '__main__':
    newspapers = [["zeit.de", "german"], ["bild.de", "german"],
                  ["theguardian.com", "english"], ["newyorker.com", "english"],
                  ["nytimes.com", "english"], ["breitbart.com", "english"]]


    Newspaper = namedtuple('Newspaper', ['url', 'language'])

    newspapers = [Newspaper(*tup) for tup in newspapers]

    parser = argparse.ArgumentParser()
    parser.add_argument('--language', default="english", nargs='?')
    parser.add_argument('--onlyopen', default="0", nargs='?')

    args = parser.parse_args()
    main(args.language, newspapers, bool(int(args.onlyopen)))
