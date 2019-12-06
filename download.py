import requests
from bs4 import BeautifulSoup
from pathlib import Path
import json
import nltk

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

def web_scraper(k):
    website = k[0]
    lang = k[1]
    links = []
    if lang == "german":
        query = "Klimawandel site:" + website

        for j in search(query, tld="co.in", num=100, start = 1, stop = 100):
            links.append(j)

    elif lang == "english":
        query = "Climate Change site:" + website

        for j in search(query, tld="co.in", num=100, start = 1, stop = 100):
            links.append(j)


    return links



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

if __name__ == '__main__':
    newspapers = [["zeit.de", "german"], ["bild.de", "german"], ["theguardian.com", "english"], ["newyorker.com", "english"], ["nytimes.com", "english"], ["breitbart.com", "english"]]

    websites = []
    for j in newspapers:
        for i in web_scraper(j):
            websites.append([j[0],i, j[1]])
    print(websites)

    for j in websites:
        text_save(j)
