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

if __name__ == "__main__":
    unittest.main()
