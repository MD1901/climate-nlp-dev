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


## What is polarity?

- honest / dishonest

- realistic / unrealistic
- deny / not deny

- future good or bad
- impacts

- upbeat, hopeless, on the right path (hope, positive, optimistic)
