import requests
from lxml.html import fromstring
import time

SEARCH_URL = 'https://duckduckgo.com/html/'
REFERER_URL = 'https://duckduckgo.com/html/'
MOZ_USER_AGENT = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, '
                  'like Gecko) Chrome/27.0.1453.93 Safari/537.36')


class FormatError(ValueError):
    """
    Raised when we believe we've failed to scrape the page because it didn't
    match the format we expected (ie if there are no results, but the page
    didn't tell us so)
    """
    pass


def search(keywords, max_results=10):
    post_data = {
        'q': keywords,
        'b': '',
    }
    headers = {'referer': REFERER_URL,
               'user-agent': MOZ_USER_AGENT}

    yielded = 0
    while True:
        res = requests.post(SEARCH_URL, data=post_data, headers=headers)
        res.raise_for_status()

        xpath_root = fromstring(res.content)
        results = extract_results(xpath_root)
        for result in results:
            yield result
            yielded += 1
            if max_results is not None and yielded >= max_results:
                return

        try:
            next_page_form = xpath_root.cssselect(
                '.results_links_more form')[-1]
        except IndexError:
            return  # no 'next' form, that's the end of the results
        post_data = dict(next_page_form.fields)
        time.sleep(3)


def extract_results(doc):
    results = [a.get('href') for a in doc.cssselect('#links .links_main > a')]
    if not len(results):
        if not no_results(doc):
            # Page has probably changed; either we've missed the
            # 'no results' span or we failed to scrape any result elements
            # from the page.
            raise FormatError(
                "No results found, but we didn't get an explicit message "
                "to that effect - the results page may have changed.")
    return results


def no_results(lxml_root):
    """
    >>> no_results(fromstring('<span class="no-results">foo</span>"'))
    True
    >>> no_results(fromstring('<html><body></body></html>'))
    False
    """
    return len(lxml_root.cssselect('span.no-results')) == 1
