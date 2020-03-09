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


def check_zeit(link):
    parts = link.split('/')

    unwanted = ['video']
    for unw in unwanted:
        if unw in parts:
            return False
        else:
            return True


def check_fox(link):
    parts = link.split('/')

    unwanted = ['category']
    for unw in unwanted:
        if unw in parts:
            return False
        else:
            return True


def check(link):
    return True


def parse_guardian(link):
    cls = 'content__article-body from-content-api js-article__body'
    html = requests.get(link).text
    soup = BeautifulSoup(html, features="html.parser")

    table = soup.findAll('div', attrs={"class": cls})

    if len(table) != 1:
        import pdb; pdb.set_trace()
    assert len(table) == 1

    article = [p.text for p in table[0].findAll('p')]
    article = ''.join(article)
    return {'body' :article, 'url': link, 'author': "", 'date': "", 'newspaper': 'guardian'}


def parse_fox(link):
    cls = 'article-body'
    html = requests.get(link).text
    soup = BeautifulSoup(html, features="html.parser")

    table = soup.findAll('div', attrs={"class": cls})
    if len(table) != 1:
        import pdb; pdb.set_trace()
    assert len(table) == 1

    article = [p.text for p in table[0].findAll('p', attrs={"class": "speakable"})]
    article = ''.join(article)
    return {'body' : article}


def parse_newyorker(link):
    cls = 'grid--item body body__container article__body grid-layout__content'
    html = requests.get(link).text
    soup = BeautifulSoup(html, features="html.parser")

    table = soup.findAll('div', attrs={"class": cls})
    if len(table) != 1:
        import pdb; pdb.set_trace()
    assert len(table) == 1

    article = [p.text for p in table[0].findAll('p')]
    article = ''.join(article)
    return {'body' : article}


def parse_bild(link):
    cls = 'txt'
    html = requests.get(link).text
    soup = BeautifulSoup(html, features="html.parser")

    table = soup.findAll('div', attrs={"class": cls})
    if len(table) != 1:
        import pdb; pdb.set_trace()
        raise ValueError(link)
    assert len(table) == 1

    article = [p.text for p in table[0].findAll('p')]
    article = ''.join(article)
    return {'body' : article}


def parse_zeit(link):
    cls = 'article-page'
    html = requests.get(link).text
    soup = BeautifulSoup(html, features="html.parser")

    table = soup.findAll('div', attrs={"class": cls})
    if len(table) != 1:
        import pdb; pdb.set_trace()
    assert len(table) == 1

    article = [p.text for p in table[0].findAll('p')]
    article = ''.join(article)
    return {'body' : article}


newspapers = [
    {
        "site": "zeit.de",
        "language": "german",
        "newspaper": "zeit",
        "checker": check_zeit,
        "parser": parse_zeit
    },
    {
        "site": "theguardian.com",
        "language": "english",
        "newspaper": "guardian",
        "checker": check_guardian,
        "parser": parse_guardian
    },
    {
        "site": "bild.de",
        "language": "german",
        "newspaper": "bild",
        "parser": parse_bild
    },
    {
        "site": "newyorker.com",
        "language": "english",
        "newspaper": "newyorker.com",
        "parser": parse_newyorker
    },
    {"site": "nytimes.com", "language": "english", "newspaper": "nytimes"},
    {
        "site": "foxnews.com",
        "language": "english",
        "newspaper": "fox",
        "checker": check_fox,
        "parser": parse_fox

    },
    {"site": "bbc.com", "language": "english", "newspaper": "bbc"},
    {"site": "theaustralian.com.au", "language": "english", "newspaper": "australian"},
    {"site": "news.sky.com/uk", "language": "english", "newspaper": "skyuk"},
    {"site": "skynews.com.au", "language": "english", "newspaper": "skyau"}
]
