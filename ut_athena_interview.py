#!/usr/bin/env python3

import unittest
from athena_interview import rank
 
class RankTests(unittest.TestCase):
    def test_1(self):
        self.assertEqual(rank("ABAB"), 2)
    def test_2(self):
        self.assertEqual(rank("AAAB"), 1)
    def test_3(self):
        self.assertEqual(rank("BAAA"), 4)
    def test_4(self):
        self.assertEqual(rank("QUESTION"), 24572)
    def test_5(self):
        self.assertEqual(rank("BOOKKEEPER"), 10743)
    def test_6(self):
        self.assertEqual(rank("ABCDEFGHIJKLMNOPQRSTUVWXY"), 1)
    def test_7(self):
        # Per the documentation (athena - Coding Challenge.revised.pdf), we shouldn't see i
        # input generating output this large. If execution time and memory footprint meet
        # the spec on this, it's a good indicator any other input will pass as well.
        self.assertEqual(rank("YXWVUTSRQPONMLKJIHGFEDCBA"), 1.5511210043330984e+25)
    def test_8(self):
        self.assertEqual(rank("BAAAAAAAAAAAAAAAAAAAAAAAA"), 25)

if __name__ == "__main__":
    unittest.main()
