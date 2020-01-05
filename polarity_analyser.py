

from collections import defaultdict
import json
import operator
from pathlib import Path

import spacy

class polarity_without_shifter:
    def __init__(self, lang):
        self.lang = lang
        polarity_sum = 0.0
        if self.lang == "english":
            self.model = spacy.load("en_core_web_sm") 
            self.polarity_dict = dict_import("english")


        else:
            self.model = spacy.load("de_core_news_sm")
            self.polarity_dict = dict_import("german")
        self.shifter_dict = shifter_import()

    def analyse(self, text):
        self.text_modeled = self.model(text)
        for sentence in self.text_modeled.sents:
            polarity_sum += sentence_polarity(sentence)
        print(str(polarity_sum) + ": " + text)
        return polarity_sum


    def sentence_polarity(self, sentence):
    polarity_sum = 0.0
    words_pol = {}
    words_shift = {}
    for word in sentence:
        if word.lemma_ in polarity_dict:
            words_pol[word] = float(polarity_dict[word.lemma_])
        else:
            words_pol[word] = 0.0
        if word.lemma_ in shifter_dict:
            words_shift[word] = shifter_dict[word.lemma_]
        else:
            words_shift[word] = "nonshifter"

    for word in reversed(sentence):
        if word.dep_ == "neg":
            polarity_sum = -0.7 * polarity_sum
        elif words_shift[word] == "shifter":
                if words_pol[word] == 0:
                    polarity_sum = -0.5 * polarity_sum
                else:
                    polarity_sum = -0.5 * polarity_sum + words_pol[word]
            elif word.dep_ == "dobj" or word.dep_ == "nsubj":
                polarity_sum += 2*words_pol[word]
            else:
                polarity_sum += float(words_pol[word])
        if not len(sentence) == 0:
            polarity_value = polarity_sum / len(sentence)
        else:
            polarity_value = 0
        return polarity_value

def dict_import(lang):
    polarity_dict = {}
    if lang in "german english":
        with open(lang + "_wordlist.txt", "r") as open_file:
            for line in open_file:
                word, value = line.split("\t")
                polarity_dict[word] = value
    else:
        return None

    return polarity_dict

def shifter_import():
    shifter_dict = {}
    with open("shifter_lemma_lexicon.csv", "r") as open_file:
        for line in open_file:
                word, value = line.replace("\n", " ").split(",")
                shifter_dict[word] = value
    return shifter_dict
