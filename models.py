"""
class Word:
    def __init__(self, text, polarity):
        self.text = text
        self.polarity = polarity

class Model:
    def analyse(self, text):
        raise NotImplementedError
"""

from collections import namedtuple

Word = namedtuple('Word', ['text', 'polarity'])


def get_simple_sentence_polarity(sentence, polarity_dict):
    # check on stop words
    return [polarity_dict.get(word, 0) for word in sentence]


class AdamSimple:
    def __init__(self, polarity_dict):
        self.polarity_dict = polarity_dict

    # untested
    def analyse(self, text):
        sentence = text.split(' ')
        sentence = [w.lower() for w in sentence]
        polarities = get_simple_sentence_polarity(sentence, self.polarity_dict)
        assert len(sentence) == len(polarities)
        return [Word(word, pol) for word, pol in zip(sentence, polarities)]
