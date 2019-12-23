"""
Task == document polarity (positive or negative article)

TDD
1. write a test
2. check the test fails
3. write fctn till it passes


Intensity
"""

import pytest
polarity_dict = {
    'abandon': -20,
    'threat': -20,
    'success': 20,
    'improve': 20,
    'sick': -20,
    'sparkle': 30,
    'son-of-a-bitch': -50,
    'hope': 20,
    'pollute': -20
}

shifting_dict = {
    'abandon': 1,
    'improve': 1,
    'threat': 1,
}


def get_simple_sentence_polarity(sentence, polarity_dict):
    # check on stop words
    return [polarity_dict.get(word, 0) for word in sentence]

@pytest.mark.parametrize(
    'sentence, expected, polarity_dict',
    [
        (('climate', 'change', 'threat', 'success'), 0, polarity_dict),
        (('climate', 'improve', 'sick'), 0, polarity_dict),
        (('sparkle', 'son-of-a-bitch'), -20, polarity_dict)
    ]
)
def test_sentence_polarity(sentence, expected, polarity_dict):
    result = get_simple_sentence_polarity(sentence, polarity_dict)
    assert expected == sum(result)


def get_simple_shifted_sentence_polarity(sentence, polarity_dict, shifting_dict):
    """
    Flips the polarity of the word before

    Improving pollution == flipped
    Improving health == flipped (!)
    """
    sentence_polarity = []
    for bef, word in zip(reversed(sentence[0:-1]), reversed(sentence[1:])):

        pol = polarity_dict.get(word, 0)
        bef_pol = polarity_dict.get(bef, 0)
        bef_shift = bool(shifting_dict.get(bef, 0))

        if bef_shift:
            pol *= -1

        sentence_polarity.append(pol)

    #  incl first word
    sentence_polarity.append(polarity_dict.get(sentence[0], 0))
    return sentence_polarity


@pytest.mark.parametrize(
    'sentence, expected, polarity_dict, shifting_dict',
    [
        (('climate', 'change', 'threat', 'success'), 0 + 0 + -20 + -1 * 20, polarity_dict, shifting_dict),
        (('climate', 'improve', 'sick'), 0 + 20 + -1 * -20, polarity_dict, shifting_dict),

        (('abandon', 'hope'), -20 + -1 * 20, polarity_dict, shifting_dict),
        (('improve', 'pollute'), 20 + -1 * -20, polarity_dict, shifting_dict),
    ]
)
def test_shifted_polarity(sentence, expected, polarity_dict, shifting_dict):
    # It is large and stylish, however, I cannot recommend it because of the lid
    # ‘I am not happy with this flashcard at all’.
    # i dont hate this city

    result = get_simple_shifted_sentence_polarity(sentence, polarity_dict, shifting_dict)
    assert expected == sum(result)
