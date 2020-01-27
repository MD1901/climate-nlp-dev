import argparse
from collections import namedtuple
import json
from pathlib import Path
import requests

from bs4 import BeautifulSoup
from googlesearch import search

def web_scraper(newspaper, num_results):
    """ returns links from a given newspaper """
    queries = {
        "german": "Klimawandel site:",
        "english": "Climate Change site:"
    }
    website, lang = newspaper
    query = queries[lang] + website
    links = [j for j in search(query, tld="co.in", num=num_results, start=1, stop=num_results)]
    return links


def save_html(article):
    newspaper = article[0]
    url = article[1]
    lang = article[2]
    response = requests.get(url)
    data_home = Path.home() / "climate-nlp" / "raw" /  newspaper.replace(".", "_")
    data_home.mkdir(parents=True, exist_ok=True)
    filename = url.split("/")[-1] + ".html"
    with open(data_home / filename, 'w') as fp:
        fp.write(response.text)

    json_text = {"url": url}
    json_filename = url.split("/")[-1] + ".json"
    with open(data_home / json_filename, 'w') as fp:
        json.dump(json_text, fp)


def import_newspapers(single=None):
    with open("listofwebsites.json", "r") as listofwebsites:
        newspapers = json.load(listofwebsites)

    newspapers = [Newspaper(tup["url"], tup["lang"]) for tup in newspapers]
    if single:
        newspapers = [n for n in newspapers if single in n.url]
    print(newspapers)
    return newspapers


def remove_links(links):

    avoids = ['bitesize', ]

    for avoid in avoids:
        links = [l for l in links if avoid not in l]

    return links


def main(language, num_results, news):
    websites = []
    for new in news:
        if new.language == language:
            links = web_scraper(new, num_results)
            links = remove_links(links)

            for link in links:
                websites.append((new.url, link, new.language))
                print(websites[-1])
                save_html(websites[-1])


Newspaper = namedtuple('Newspaper', ['url', 'language'])
if __name__ == '__main__':
    newspapers = import_newspapers('fox')
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', default="english", nargs='?')
    parser.add_argument('--number', default="150", nargs='?')

    args = parser.parse_args()
    main(args.language, int(args.number), newspapers)
