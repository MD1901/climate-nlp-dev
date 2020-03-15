import argparse
from collections import defaultdict
import json
from pathlib import Path
import requests

from bs4 import BeautifulSoup
from googlesearch import search

from newspapers import newspapers as all_newspapers


def get_newspapers(newspapers):
    return [n for n in all_newspapers if n['newspaper'] in newspapers]


def get_newspaper_links(newspaper, num_results):
    """ returns links from a given newspaper """
    queries = {
        "german": "klimawandel site:",
        "english": "climate change site:"
    }
    lang = newspaper['language']
    website = newspaper['site']
    print('scraping {}'.format(newspaper['newspaper']))

    query = queries[lang] + website
    links = [j for j in search(
        query,
        tld="co.in",
        num=num_results,  # do we need this?
        start=1,
        stop=num_results,
        pause=2.0,
        user_agent='adam'
    )]
    return links


def check_links(links, newspaper):
    if "checker" in newspaper:
        check = newspaper["checker"]
        return [l for l in links if check(l)]
    else:
        return links


def parse_link(link, newspaper):
    if "parser" in newspaper:
        parser = newspaper["parser"]
        parsed = parser(link)

        parsed['id'] = link.split('/')[-1]
        parsed['newspaper'] = newspaper['newspaper']
        parsed['link'] = link
        return parsed
    else:
        return link


class TextFiles:
    def __init__(self, root):
        self.root = Path.home() / 'climate-nlp' / root
        self.root.mkdir(parents=True, exist_ok=True)

    def post(self, data, fi):
        fi = self.root / fi
        with open(fi, 'w') as fp:
            fp.write(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--newspapers',
        default="guardian",
        nargs='*'
    )
    parser.add_argument(
        '--num',
        default=2,
        nargs='?',
        type=int
    )
    args = parser.parse_args()
    print(args)

    newspapers = args.newspapers
    newspapers = get_newspapers(newspapers)
    print(newspapers)
    raw = TextFiles('raw')
    interim = TextFiles('interim')

    articles = defaultdict(list)
    for newspaper in newspapers:
        links = get_newspaper_links(newspaper, args.num)
        links = check_links(links, newspaper)

        for link in links:
            # html = requests.get(link, 'html.parser').text
            parsed = parse_link(link, newspaper)
            fname = parsed['id']
            raw.post(parsed['html'], str(fname)+'.html')
            interim.post(json.dumps(parsed), str(fname)+'.json')
