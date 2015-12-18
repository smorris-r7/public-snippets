#!/usr/bin/env python3

import argparse
import logging
import sys
import math

def evaluate(letters):
    """
    Rank a word alphabetically against all possible permutations of its letters. The earliest perm gets a rank of 1.
    The latest perm gets a rank of factorial(len(word)). If the word contains duplicate letters, return the lowest
    possible rank. Execution time must beat 500 ms and memory used must stay under 1 GB.
    """
    logging.debug("letters: {0}".format(letters))
    remaining = list(letters)
    remaining.sort()
    logging.debug("remaining: {0}".format(remaining))
    total_branches_to_left = 0
    for letter in letters:
        logging.debug("* * * * * * * * * * * * *")
        logging.debug("processing letter {0}...".format(letter))
        
        next_branches = math.factorial(len(remaining)-1)
        logging.debug("next_branches:      {0}".format(next_branches))
        index_in_remaining = remaining.index(letter)
        logging.debug("index_in_remaining: {0}".format(index_in_remaining))
        branches_to_left = index_in_remaining * next_branches
        logging.debug("branches_to_left:   {0}".format(branches_to_left))
        total_branches_to_left += branches_to_left

        remaining.remove(letter)
    logging.debug("total_branches_to_left: {0}".format(total_branches_to_left))
    rank = total_branches_to_left + 1
    return rank 

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("--word", help="a 25 letter or less word to evaluate", required=True)
    args = parser.parse_args()
    word = list(args.word)

    rank = evaluate(word)
    print(rank)
