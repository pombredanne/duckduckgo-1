#!/usr/bin/env python

import unittest
import duckduckgo
import lxml.html

from os.path import join, dirname, abspath
SAMPLE_DIR = abspath(join(dirname(__file__), 'sample_data'))


class DuckDuckGoParserTest(unittest.TestCase):
    def test_extract_results(self):
        with open(join(SAMPLE_DIR, 'results_test.html'), 'r') as f:
            lxml_root = lxml.html.fromstring(f.read())
            self.assertEqual(26, len(duckduckgo.extract_results(lxml_root)))

    def test_dont_extract_these_results(self):
        """
        duckduckgo suggests using google or bing if it doesn't return any
        results - we mustn't mistake these urls for actual search results.
        """
        with open(join(SAMPLE_DIR, 'no_results.html'), 'r') as f:
            lxml_root = lxml.html.fromstring(f.read())
            self.assertEqual(0, len(duckduckgo.extract_results(lxml_root)))

    def no_results_positive(self):
        with open(join(SAMPLE_DIR, 'no_results.html'), 'r') as f:
            lxml_root = lxml.html.fromstring(f.read())
            self.assertEqual(True, duckduckgo.no_results(lxml_root))

    def no_results_negative(self):
        with open(join(SAMPLE_DIR, 'results_tests.html'), 'r') as f:
            lxml_root = lxml.html.fromstring(f.read())
            self.assertEqual(Fa,se, duckduckgo.no_results(lxml_root))


class DuckDuckGoLiveTest(unittest.TestCase):
    def test_detect_no_results(self):
        """
        Check that we correctly identify a 'no results' situation from the
        live search engine.
        """
        noresults = "\"%s\"" % "".join(['fjdka', 'fdasfda', 'toitjfg'])
        self.assertEqual([],
                         list(duckduckgo.search(noresults, max_results=5)))

    def test_get_some_results(self):
        """
        Check that we're actually getting some URLS for a common search term.
        """
        results = list(duckduckgo.search('test', max_results=5))
        self.assertEqual(5, len(results))


