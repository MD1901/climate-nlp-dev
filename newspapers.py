from bs4 import BeautifulSoup
import requests

"""
https://www.theguardian.com/sustainable-business/blog/environment-climate-change-denier-global-warming
'https://www.theguardian.com/environment/2011/apr/21/countries-responsible-climate-change'
"""


def check_guardian(link):
    parts = link.split('/')

    unwanted = ['live', 'gallery', 'audio', 'video', 'ng-interactive', 'interactive']
    for unw in unwanted:
        if unw in parts:
            return False

    try:
        #  check if there is a year / str / day
        #  can be in one of two positions
        cond1 = parts[4].isdigit() and parts[6].isdigit()
        cond2 = parts[5].isdigit() and parts[7].isdigit()

        if cond1 or cond2:
            return True
        else:
            print('rejecting {}'.format(link))
            return False

    #  short link
    except IndexError:
        print('rejecting {}'.format(link))
        return False


def check(link):
    return True


def parse_guardian(link):
    cls = 'content__article-body from-content-api js-article__body'

    fname = link.split('/')[-1]
    html = requests.get(link).text
    soup = BeautifulSoup(html, features="html.parser")

    table = soup.findAll('div', attrs={"class": cls})

    if len(table) != 1:
        import pdb; pdb.set_trace()
    assert len(table) == 1

    article = [p.text for p in table[0].findAll('p')]
    article = ''.join(article)
    return {'body' :article, 'url': link, 'author': "", 'date': "", 'newspaper': 'guardian', 'id': fname}


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


