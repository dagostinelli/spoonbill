import unittest
import spoonbill


class TestCompile(unittest.TestCase):

	def test_sanity_1(self):
		x = spoonbill.compile('example-data/example1.md', 'example-data', 'example-data/', None, {'template': 'default.html'})
		self.assertTrue(x)

	def test_sanity_fragment1(self):
		x = spoonbill.compile('example-data/example2.md', 'example-data', 'example-data/', None, {'template': 'default.html'})
		print(x)
		# x = True
		self.assertTrue(x)
