# Climate-nlp

Development of climate NLP tools.  Currently developing two tools:
1. download & parse of climate change newspaper articles
2. polarity labelling of newspaper articles

## Download & parse

Uses the newspaper information in `newspapers.py`.

```bash
/Users/adam/climate-nlp
├── final
├── interim
└── raw
```

Will download the HTML into `~/climate-nlp/raw` and parse the article into `.txt` in `~/climate-nlp/interim`:

```bash
python download.py --newspaper --num
```

