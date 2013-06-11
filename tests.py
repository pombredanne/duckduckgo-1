import unittest
import duckduckgo
import random
import string


class DuckDuckGoTest(unittest.TestCase):
    def test_detect_no_results(self):
        random_string = "".join([
            random.choice(string.ascii_letters) for n in xrange(30)])

        self.assertRaises(
            duckduckgo.NoResultsException,
            lambda: duckduckgo.search("\"%s\"" % random_string))

    def test_some_results(self):
        results = list(duckduckgo.search('test', max_results=5))
        self.assertEqual(5, len(results))
