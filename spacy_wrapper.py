from spacy.lang.en import English
from spacy.tokenizer import Tokenizer
from spacy.matcher import Matcher
import spacy

def get_merger(nlp):

    def merger(doc):
        # https://stackoverflow.com/questions/50752266/spacy-tokenize-quoted-string/50775597#50775597
        matcher = Matcher(nlp.vocab)
        pattern = [{'LOWER': 'climate'}, {'LOWER': 'change'}]
        matcher.add('cc', None, pattern)

        pattern = [{'LOWER': 'fossil'}, {'LOWER': 'fuel'}]
        matcher.add('ff', None, pattern)

        spans = []
        for m_id, s, e in matcher(doc):
            spans.append(doc[s:e])

        for span in spans:
            span.merge()
        return doc

    return merger


def load_spacy_wrapper(lang, version='custom'):
    print('loading spacy wrapper {} {}'.format(lang, version))
    nlp = spacy.load('en_core_web_sm')
    if version == 'standard':
        return nlp
    else:
        merger = get_merger(nlp)
        nlp.add_pipe(merger, first=True)
        return nlp


if __name__ == '__main__':
    nlp = load_spacy_wrapper('english')
    text = 'climate change is bad fossil fuel climate fossil'
    doc = nlp(text)
    tokes = [t for t in doc]
    print(tokes)
