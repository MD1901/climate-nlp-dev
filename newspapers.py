from bs4 import BeautifulSoup
import requests


def check_guardian(link):
    #  see if the year
    try:
        int(link.split('/')[4])  # year
        int(link.split('/')[6])  # day
        return True
    except ValueError:
        print('rejecting {}'.format(link))
        return False


def check(link):
    return link


def parse_guardian(link):

    cls = 'content__article-body from-content-api js-article__body'
    html = requests.get(link).text
    soup = BeautifulSoup(html, features="html.parser")

    table = soup.findAll('div', attrs={"class": cls})
    assert len(table) == 1

    article = [p.text for p in table[0].findAll('p')]
    article = ''.join(article)
    return article


newspapers = [
    {"site": "zeit.de","language": "german", "id": "zeit"},
    {
        "site": "theguardian.com",
        "language": "english",
        "id": "guardian",
        "checker": check_guardian,
        "parser": parse_guardian
    },
    {"site": "bild.de", "language": "german", "id": "bild"},
    {"site": "newyorker.com","language": "english", "id": "newyorker.com"},
    {"site": "nytimes.com", "language": "english", "id": "nytimes"},
    {
        "site": "foxnews.com",
        "language": "english",
        "id": "fox",
        "checker": check
    },
    {"site": "bbc.com", "language": "english", "id": "bbc"},
    {"site": "theaustralian.com.au", "language": "english", "id": "australian"},
    {"site": "news.sky.com/uk", "language": "english", "id": "skyuk"},
    {"site": "skynews.com.au", "language": "english", "id": "skyau"}
]


