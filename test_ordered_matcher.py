import unittest

from ordered_matcher import Matcher
from patterns import BlankPattern, RawPattern, BlankSequencePattern


def matchQ(patts, args):
    m = Matcher(patts, args)
    return m.match()


class MatchTest(unittest.TestCase):
    def assertMatchTrue(self, patts, args):
        self.assertTrue(matchQ(patts, args))

    def assertMatchFalse(self, patts, args):
        self.assertFalse(matchQ(patts, args))

    def test_blank(self):
        self.assertMatchTrue([BlankPattern('x')], [1])
        self.assertMatchTrue([BlankPattern('x'), BlankPattern('y')], [1, 2])

    def test_blank_none(self):
        self.assertMatchFalse([BlankPattern('x')], [])

    def test_blank_too_many(self):
        self.assertMatchFalse([BlankPattern('x')], [1, 2])
        self.assertMatchFalse([BlankPattern('x'), BlankPattern('y')], [1, 2, 3])

    def test_blanksequence(self):
        self.assertMatchTrue([BlankSequencePattern('x')], [1])
        self.assertMatchTrue([BlankSequencePattern('x')], [1, 2])
        self.assertMatchTrue([BlankSequencePattern('x')], [1, 2, 3])

    def test_blanksequence_multi(self):
        self.assertMatchFalse([BlankSequencePattern('x'), BlankSequencePattern('y')], [])
        self.assertMatchFalse([BlankSequencePattern('x'), BlankSequencePattern('y')], [1])
        self.assertMatchTrue([BlankSequencePattern('x'), BlankSequencePattern('y')], [1, 2])
        self.assertMatchTrue([BlankSequencePattern('x'), BlankSequencePattern('y')], [1, 2, 3])
        self.assertMatchTrue([BlankSequencePattern('x'), BlankSequencePattern('y')], [1, 2, 3, 4, 5])

    def test_blanksequence_none(self):
        self.assertMatchFalse([BlankSequencePattern('x')], [])

    def test_raw(self):
        self.assertMatchTrue([RawPattern('x', 1)], [1])

    def test_raw_blank(self):
        self.assertMatchFalse([BlankPattern('x'), BlankPattern('y'), RawPattern('z', 1)], [1, 2, 3])
        self.assertMatchTrue([BlankPattern('x'), BlankPattern('y'), RawPattern('z', 1)], [3, 2, 1])
