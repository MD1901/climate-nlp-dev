"""
class Word:
    def __init__(self, text, polarity):
        self.text = text
        self.polarity = polarity

class Model:
    def analyse(self, text):
        raise NotImplementedError
"""
from collections import defaultdict, namedtuple
import json
import operator
from pathlib import Path

import spacy


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


class Polarity():

    def __init__(self, lang):
        self.lang = lang

    def analyse(self, text):
        polarity_sum = 0.0
        polarity_list = []
        sentences = text.split(".")
        for sentence in sentences:
            words = sentence.split(" ")
            polarity_list.append(self.sentence_polarity(words))
            polarity_sum += sum(self.sentence_polarity(words))
        if not len(text) == 0:
            polarity_sum = polarity_sum / len(text)
        else:
            polarity_sum = 0
        print(str(polarity_sum) + ": " + text)
        print(polarity_list)
        return polarity_sum, polarity_list

    def sentence_polarity(self, sentence):
        polarity_list = []
        for word in sentence:
            polarity_list.append( which_polarity(word, self.lang))
            print(word + ": " + str(which_polarity(word, self.lang)))

        return polarity_list


class PolarityWithNeg(Polarity):
    def __init__(self, lang):
        self.lang = lang

    def sentence_polarity(self, sentence):
        polarity_list = []

        for word in reversed(sentence):
            if is_neg(word, self.lang) == "neg":
                polarity_list[-1] *= polarity_sum
            else:
                polarity_list.append(which_polarity(word, self.lang))

        return polarity_list


class PolarityWithIntens(Polarity):

    def sentence_polarity(self, sentence):
        polarity_list = []
        polarity_list.append(which_polarity(word, self.lang))
        polarity_list[-1] *= which_intens(word, self.lang)

        return polarity_list


class PolarityWithNegWithIntens(Polarity):
    def __init__(self, lang):
        self.lang = lang

    def sentence_polarity(self, sentence):
        polarity_list = []

        for word in reversed(sentence):
            if is_neg(word, self.lang) == "neg":
                polarity_list[-1] = polarity_list[-1] * polarity_sum
            else:
                polarity_list.append(which_polarity(word, self.lang))
                polarity_list[-1] *= which_intens(word, self.lang)

        return polarity_list


class PolarityWithNegWithSpacy(Polarity):
    def __init__(self, lang):
        self.lang = lang
    def analyse(self, text):
        polarity_sum = 0.0
        text_modeled = model(text)
        for sentence in self.text_modeled.sents:
            polarity_sum += self.sentence_polarity(sentence)
        if not len(text) == 0:
            polarity_sum = polarity_sum / len(text)
        else:
            polarity_sum = 0
        print(str(polarity_sum) + ": " + text)
        return polarity_sum

    def sentence_polarity(self, sentence):
        polarity_sum = 0.0
        for word in reversed(sentence):
            if word.dep_== "neg":
                polarity_sum = -0.7 * polarity_sum
            else:
                polarity_sum += which_polarity(word.lemma_)
        return polarity_sum

def is_neg(word,language = "english"):
        if language == "german":
            neg_dict = dict_import("german", "neg")
        else:
            neg_dict = dict_import("english", "neg")

        if word in neg_dict:
            return True
        else:
            return False

def which_intens(word,language = "english"):
        if language == "german":
            intens_dict = dict_import("german", "intens")
        else:
            intens_dict = dict_import("english", "intens")

        if word in intens_dict:
            return intens_dict[word]
        else:
            return 1

def which_polarity(word,language = "english"):
        if language == "german":
            pol_dict = dict_import("german")
        else:
            pol_dict = dict_import("english")
        if word in pol_dict:
            return pol_dict[word]
        else:
            return 0


def dict_import(lang, other_mode = ""):
    if other_mode == "neg":
        neg_list = []
        if lang in "german,english":
            with open("/lexica/" + lang + "/negation.txt", "r") as open_file:
                for line in open_file:
                    neg_list.append(line.replace("\n", ""))
            return neg_list
        else:
            return None
    if other_mode == "intens":
        intens_dict = {}
        if lang in "german,english":
            with open("/lexica/" + lang + "/intensity.txt", "r") as open_file:
                for line in open_file:
                    word, value = line.replace("\n", "").split("\t")
                    intens_dict[word] = int(value)
            return intens_dict
        else:
            return None
    else:
        polarity_dict = {}
        if lang in "german,english":
            print("language:" + lang)
            #with open("/lexica/" + lang + "/polarity.txt", "r") as open_file:
            #    for line in open_file:
            #        word, value = line.replace("\n", "").split("\t")
            #        polarity_dict[word] = int(value)
        else:
            return None

    return polarity_dict
