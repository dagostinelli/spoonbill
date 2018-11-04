import unittest


class TestMyClass(unittest.TestCase):

    def test_x(self):
        self.assertEqual(1, 1)

    def test_y(self):
        self.assertEqual(2, 2)

    def test_z(self):
        self.assertEqual(3, 3)
