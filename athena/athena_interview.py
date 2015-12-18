#!/usr/bin/env python3

"""athena_interview.py: An implementation of 'athena - Coding Challenge.revised.pdf'."""

__author__ = "Sam Morris"

import argparse
import logging
import math
import collections
import string

def validate_input(unvalidated):
    """
    Verify input is a nonempty list of characters A..Z of length less than or equal to 25.
    Duplicate elements are permissable.
    """
    try:
        length = len(unvalidated)
        assert 1 <= length <= 25
        for element in unvalidated:
            assert element in string.ascii_uppercase
    except:
        # don't bother to handle bad input and continue executing, just raise the exception
        raise

def rank(letters):
    """
    Rank a word (given as a list of letters) alphabetically against all possible permutations
    of its letters. The earliest perm gets a rank of 1, and the last perm gets a rank of
    factorial(len(letters))/product(factorials of the counts of all duplicate letters).
    Execution time must beat 500 ms and memory used must stay under 1 GB.
    """
    logging.debug("letters: {0}".format(letters))
    remaining = list(letters)
    remaining.sort()
    logging.debug("remaining: {0}".format(remaining))

    total_earlier_permutations = 0
    for letter in letters:
        logging.debug("processing letter {0}...".format(letter))
        
        index_in_remaining = remaining.index(letter)
        logging.debug("index_in_remaining: {0}".format(index_in_remaining))
        earlier_permutations = math.factorial(len(remaining)-1) * index_in_remaining
        logging.debug("earlier_permutations: {0}".format(earlier_permutations))
        dupe_factor = 1
        dupe_dict = collections.Counter(remaining)
        for key in dupe_dict:
            dupe_factor *= math.factorial(dupe_dict[key])
        logging.debug("dupe_factor: {0}".format(dupe_factor))
        dupe_free_earlier_permutations = earlier_permutations / dupe_factor
        logging.debug("dupe_free_earlier_permutations: {0}".format(dupe_free_earlier_permutations))
        assert dupe_free_earlier_permutations % 1 == 0, "dupe_free_earlier_permutations is not a whole number"
        total_earlier_permutations += dupe_free_earlier_permutations

        remaining.remove(letter)
    logging.debug("total_earlier_permutations: {0}".format(total_earlier_permutations))

    final_rank = int(total_earlier_permutations + 1)
    return final_rank 

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("word", nargs='?', help="a 25 letter or less word to evaluate")
    args = parser.parse_args()
    assert args.word is not None, \
        "a positional argument is required, see --help"
    word = list(args.word)

    validate_input(word)

    r = rank(word)
    print(r)
