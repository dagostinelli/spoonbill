import unittest


class TestMySecondClass(unittest.TestCase):

    def test_p(self):
        self.assertEqual(1, 1)

    def test_d(self):
        self.assertEqual(2, 2)

    def test_q(self):
        self.assertEqual(3, 3)
