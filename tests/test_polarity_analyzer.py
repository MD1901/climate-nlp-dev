import polarity_analyser


def test_polarity_without_shifter():
    model = polarity_analyser.Polarity(
        "Das hier ist der erste Testsatz"
    )


def text_polarity_with_shifter_other_lexicon():
    model = polarity_analyser.Polarity(
        "Das hier ist der erste Testsatz",
        True
    )
