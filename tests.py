import unittest
import duckduckgo

class DuckDuckGoTest(unittest.TestCase):
    def test_detect_no_results(self):
        self.assertRaises(
            duckduckgo.NoResultsException,
            lambda: duckduckgo.search('"noresultsshouldbefound"'))

    def test_some_results(self):
        results = list(duckduckgo.search('test', max_results=5))
        self.assertEqual(5, len(results))
