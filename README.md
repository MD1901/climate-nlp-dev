# Climate-nlp

Development of climate NLP tools.  Currently developing two tools:
1. download & parse of climate change newspaper articles
2. polarity labelling of newspaper articles

## newspapers.py

Each newspaper has a parser function, returns `.json`

## download.py

Does both downloading and parsing

Uses the newspaper information in `newspapers.py`.

```bash
/Users/adam/climate-nlp
├── final
├── interim
└── raw
```

Will download the HTML into `~/climate-nlp/raw` and parse the article into `.json` in `~/climate-nlp/interim`:

```bash
python download.py --newspaper --num
```

Basic process
- get links from google search
- check for unwanted
- parse using newspaper parser

`grep -rl '"newspaper": "bild"' .`

Count number of `json` in `interim`:

```bash
ls ~/climate-nlp/interim | wc -l
```

## Corpus analysis

Word counter (removes stops & lemmatizes):

```bash
python count.py && less ~/climate-nlp/spacy-counts.csv

sort -k2 -t, -nr ~/climate-nlp/wordlisten-adg.csv | less
```
