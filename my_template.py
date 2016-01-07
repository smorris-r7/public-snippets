#!/usr/bin/env python3

"""my_template.py: A template python file."""

__author__ = "Sam Morris"

import argparse
import logging
import math
import collections
import string

class MyClass:
    """
    template class
    """

    def __init__(self, x):
        self.x = x

    def __iter__(self):
        return self

    def __next__(self):
        return x+1

    def __str__(self):
        return str(self)

def validate_input(unvalidated):
    """
    input validation function
    """

    try:
        length = len(unvalidated)
        assert 1 <= length <= 25
        for element in unvalidated:
            assert element in string.ascii_uppercase
    except:
        # don't bother to handle bad input and continue executing, just raise the exception
        raise


if __name__ == "__main__":
    # DEBUG, INFO, WARNING, ERROR, CRITICAL
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("word", nargs='?', help="a 25 letter or less word to evaluate")
    args = parser.parse_args()
    assert args.word is not None, \
        "a positional argument is required, see --help"
    word = list(args.word)

    validate_input(word)
