import requests
from lxml import html
import time

class NoResultsException(Exception):
    pass


def search(keywords, max_results=None):
    url = 'http://duckduckgo.com/html/'
    params = {
        'q': keywords,
        's': '0',
    }

    yielded = 0
    while True:
        res = requests.post(url, params=params)
        doc = html.fromstring(res.content)

        results = [a.get('href') for a in
                   doc.cssselect('#links .links_main a')]
        for result in results:
            yield result
            time.sleep(0.1)
            yielded += 1
            if max_results and yielded >= max_results:
                return

        try:
            form = doc.cssselect('.results_links_more form')[-1]
        except IndexError:
            return
        params = dict(form.fields)
