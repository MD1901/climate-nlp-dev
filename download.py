import json
from pathlib import Path
import requests

from bs4 import BeautifulSoup
from googlesearch import search
import nltk




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


def parse_guardian(soup):

    return text

newspaper_parsers = {
    "guardian": parse_guardian
}

parser = newspaper_parsers[lang]



def text_save(h):
    print(h)
    newspaper = h[0]
    url = h[1]
    lang = h[2]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    data = []
    date = ""
    author = ""
    if newspaper == "theguardian.com":
        for p in soup.find_all("p"):
            try:
                p["class"]
            except KeyError:
                data.append(p.text)

    else:
        for p in soup.find_all("p"):
            data.append(p.text)
    for t in soup.find_all("time"):
        try:
            date = t["datetime"]
            print(date)
            break
        except KeyError:
            break
    new = ""
    for d in data:
        new += " " + d
    """ Unterordner für climate-nlp RAW"""
    data_home = Path.home() / "climate-nlp" / newspaper.replace(".","_")
    data_home.mkdir(parents=True, exist_ok=True)

    result = {
        "url": url,
        "body": new,
        "date": date,
        "author": author,
        "lang": lang
    }
    filename = url.replace(".", "").replace(":","").replace("/","").replace("@","") + ".json"
    with open(data_home / filename, 'w') as fp:
        json.dump(result, fp)


def main(language, newspapers):
    websites = []
    for news in newspapers:
        if news.language == language:
            links = web_scraper(news)

            for link in links:
                websites.append((news.url, links, news.language))
                print(websites[-1])
                text_save(websites[-1])

if __name__ == '__main__':
    newspapers = [["zeit.de", "german"], ["bild.de", "german"], ["theguardian.com", "english"], ["newyorker.com", "english"], ["nytimes.com", "english"], ["breitbart.com", "english"]]

    from collections import namedtuple

    Newspaper = namedtuple('Newspaper', ['url', 'language'])

    newspapers = [Newspaper(*tup) for tup in newspapers]

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', default="german", nargs='?')
    args = parser.parse_args()

    main(args.language, newspapers)

