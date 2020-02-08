"""
Task == document polarity (positive or negative article)

TDD
1. write a test
2. check the test fails
3. write fctn till it passes


Intensity

todo == dobule negatives NO (shouldn't happen a lot in newspapers)

Assuming ’ -> '
"""

import pytest

from models import AdamSimple, get_simple_sentence_polarity


polarity_dict = {
    'success': 20,
    'improve': 20,
    'sick': -20,
    'sparkle': 30,
    'son-of-a-bitch': -50,
    'hope': 20,
    'pollute': -20,
    'fail': -20
}


@pytest.mark.parametrize(
    'sentence, expected, polarity_dict',
    [
        (('climate', 'change', 'success'), 20, polarity_dict),
        (('climate', 'improve', 'sick'), 0, polarity_dict),
        (('sparkle', 'son-of-a-bitch'), -20, polarity_dict)
    ]
)
def test_simple_sentence_polarity(sentence, expected, polarity_dict):
    result = get_simple_sentence_polarity(sentence, polarity_dict)
    assert expected == sum(result)
    assert len(result) == len(sentence)


# Intensity from 0 - 1.0
negation_dict = {
    'never': 1.0,
    'abandon': 0.9,
    'threat': 0.8,
    "can't": 0.5
}


@pytest.mark.parametrize(
    'sentence, expected, polarity_dict, negation_dict',
    [
        (('never', 'fail'), -1 * -20, polarity_dict, negation_dict),
        (('abandon', 'hope'), -0.9 * 20, polarity_dict, negation_dict),
        (('threat', 'success'), -0.8 * 20, polarity_dict, negation_dict),
        (("can't", 'fail'), - 0.5 * -20, polarity_dict, negation_dict),
        (("can't", 'improve'), 0.5 * -20, polarity_dict, negation_dict)
    ]
)
def test_simple_negation(sentence, expected, polarity_dict, negation_dict):
    # It is large and stylish, however, I cannot recommend it because of the lid
    # ‘I am not happy with this flashcard at all’.
    # i dont hate this city
    # (('climate', 'change', 'threat', 'success'), 0 + 0 + -20 + -1 * 20, polarity_dict, shifting_dict),
    # (('climate', 'improve', 'sick'), 0 + 20 + -1 * -20, polarity_dict, shifting_dict),

    # (('improve', 'pollute'), 20 + -1 * -20, polarity_dict, shifting_dict),

    result = simple_negation(sentence, polarity_dict, negation_dict)
    assert expected == sum(result)
    assert len(result) == len(sentence)


def simple_negation(sentence, polarity_dict, negation_dict):
    """
    Negates the next word in the sentence
    """
    sentence_polarity = [polarity_dict.get(sentence[0], 0), ]
    for first, second in zip(sentence[0:-1], sentence[1:]):

        first_pol = polarity_dict.get(first, 0)
        second_pol = polarity_dict.get(second, 0)

        if bool(negation_dict.get(first, 0)):
            second_pol *= - negation_dict.get(first, 0)

        sentence_polarity.append(second_pol)

    return sentence_polarity
