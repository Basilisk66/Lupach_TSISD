import unittest

from main import first_mismatch_index, is_balanced


class TestIsBalanced(unittest.TestCase):
    def test_empty_string_is_balanced(self):
        self.assertTrue(is_balanced(""))

    def test_simple_balanced(self):
        self.assertTrue(is_balanced("()"))
        self.assertTrue(is_balanced("fsd(выа(13)33)вы"))
        self.assertTrue(is_balanced("42cds(das)442выф(вф)0"))

    def test_extra_closing_is_unbalanced(self):
        self.assertFalse(is_balanced("32(234)sv)sd"))
        self.assertFalse(is_balanced("sci)(d"))

    def test_missing_closing_is_unbalanced(self):
        self.assertFalse(is_balanced("(23(ca)"))
        self.assertFalse(is_balanced("cd(31"))


class TestFirstMismatchIndex(unittest.TestCase):
    def test_balanced_returns_none(self):
        self.assertIsNone(first_mismatch_index(""))
        self.assertIsNone(first_mismatch_index("42(fsf(sf)3)"))

    def test_extra_closing_returns_its_index(self):
        self.assertEqual(first_mismatch_index("52(3)cx)gfgsd"), 7)
        self.assertEqual(first_mismatch_index(")fdg6"), 0)
        self.assertEqual(first_mismatch_index("pz(vl)35)(fds(df)"), 8)

    def test_missing_closing_returns_len(self):
        self.assertEqual(first_mismatch_index("fs(v(46)"), 8)
        self.assertEqual(first_mismatch_index("("), 1)
        self.assertEqual(first_mismatch_index("((()"), 4)
