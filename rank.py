#!/usr/bin/env python3

import argparse
import sys
import math

def evaluate(letters):
    """
    Rank a word alphabetically against all possible permutations of its letters. The earliest perm gets a rank of 1.
    The latest perm gets a rank of factorial(len(word)). If the word contains duplicate letters, return the lowest
    possible rank. Execution time must beat 500 ms and memory used must stay under 1 GB.
    """
    if sys.flags.debug:
        print("letters: {0}".format(letters))
        print("remaining: {0}".format(remaining))
    for letter in letters:
        if sys.flags.debug:
            print("letter: {0}".format(letter))
            #print("next_branches (len(remaining)-1)!: {0}".format(math.factorial(len(remaining)-1)))
            #print("index_in_remaining: {0}".format(remaining.index(letter)))
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--word", help="a 25 letter or less word to evaluate", required=True)
    args = parser.parse_args()
    word = args.word

    evaluate(word)
