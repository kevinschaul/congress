import unittest

import nominations

class NominationsList(unittest.TestCase):
    def test_get_page_url_simple(self):
        # Allow string representation of congress
        congress = "115"
        expected = "https://www.congress.gov/search?q=%7B%22source%22%3A%22nominations%22%2C%22congress%22%3A%22115%22%7D&pageSort=actionDesc&page=1&pageSize=250"

        result = nominations.get_page_url(congress)
        self.assertEqual(expected, result)

    def test_get_page_url_integer(self):
        # Allow integer representation of congress
        congress = 115
        expected = "https://www.congress.gov/search?q=%7B%22source%22%3A%22nominations%22%2C%22congress%22%3A%22115%22%7D&pageSort=actionDesc&page=1&pageSize=250"

        result = nominations.get_page_url(congress)
        self.assertEqual(expected, result)

    def test_get_page_url_integer(self):
        # Allow integer representation of congress
        congress = 114
        page = 3
        expected = "https://www.congress.gov/search?q=%7B%22source%22%3A%22nominations%22%2C%22congress%22%3A%22114%22%7D&pageSort=actionDesc&page=3&pageSize=250"

        result = nominations.get_page_url(congress, page)
        self.assertEqual(expected, result)

    def test_next_page_exists_true(self):
        html = """
        <div id="main">
            <ol></ol>
            <div class="nav-pag-top" role="navigation">
                <div class="pagination"><a class="first" href="/search?q=%7B%22source%22%3A%22nominations%22%2C%22congress%22%3A%22114%22%7D&amp;pageSort=actionDesc&amp;pageSize=25&amp;page=1"><i></i><span>First Page</span></a><span class="skip-back off" aria-hidden="true" aria-label="Skip Back Five Pages"><i></i></span><a class="prev" href="/search?q=%7B%22source%22%3A%22nominations%22%2C%22congress%22%3A%22114%22%7D&amp;pageSort=actionDesc&amp;pageSize=25&amp;page=2"><i></i><span>Previous Page</span></a><a href="/search?q=%7B%22source%22%3A%22nominations%22%2C%22congress%22%3A%22114%22%7D&amp;pageSort=actionDesc&amp;pageSize=25&amp;page=1">1</a><a href="/search?q=%7B%22source%22%3A%22nominations%22%2C%22congress%22%3A%22114%22%7D&amp;pageSort=actionDesc&amp;pageSize=25&amp;page=2">2</a><span class="selected" aria-label="Page 3">3</span><a href="/search?q=%7B%22source%22%3A%22nominations%22%2C%22congress%22%3A%22114%22%7D&amp;pageSort=actionDesc&amp;pageSize=25&amp;page=4">4</a><a href="/search?q=%7B%22source%22%3A%22nominations%22%2C%22congress%22%3A%22114%22%7D&amp;pageSort=actionDesc&amp;pageSize=25&amp;page=5">5</a><a class="next" href="/search?q=%7B%22source%22%3A%22nominations%22%2C%22congress%22%3A%22114%22%7D&amp;pageSort=actionDesc&amp;pageSize=25&amp;page=4"><span>Next Page</span><i></i></a><a class="skip-ahead" href="/search?q=%7B%22source%22%3A%22nominations%22%2C%22congress%22%3A%22114%22%7D&amp;pageSort=actionDesc&amp;pageSize=25&amp;page=8"><i></i><span>Skip Ahead Five Pages</span></a><a class="last" href="/search?q=%7B%22source%22%3A%22nominations%22%2C%22congress%22%3A%22114%22%7D&amp;pageSort=actionDesc&amp;pageSize=25&amp;page=78"><i></i><span>Last Page</span></a></div>
            </div>
        </div>
        """
        expected = True

        result = nominations.next_page_exists(html)
        self.assertEqual(expected, result)

    def test_next_page_exists_false(self):
        html = """
        <div id="main">
            <ol></ol>
            <div class="nav-pag-top" role="navigation">
                <div class="pagination"><a class="first" href="/search?q=%7B%22source%22%3A%22nominations%22%2C%22congress%22%3A%22114%22%7D&amp;pageSort=actionDesc&amp;pageSize=25&amp;page=1"><i></i><span>First Page</span></a><a class="skip-back" href="/search?q=%7B%22source%22%3A%22nominations%22%2C%22congress%22%3A%22114%22%7D&amp;pageSort=actionDesc&amp;pageSize=25&amp;page=73"><i></i><span>Skip Back Five Pages</span></a><a class="prev" href="/search?q=%7B%22source%22%3A%22nominations%22%2C%22congress%22%3A%22114%22%7D&amp;pageSort=actionDesc&amp;pageSize=25&amp;page=77"><i></i><span>Previous Page</span></a><a href="/search?q=%7B%22source%22%3A%22nominations%22%2C%22congress%22%3A%22114%22%7D&amp;pageSort=actionDesc&amp;pageSize=25&amp;page=74">74</a><a href="/search?q=%7B%22source%22%3A%22nominations%22%2C%22congress%22%3A%22114%22%7D&amp;pageSort=actionDesc&amp;pageSize=25&amp;page=75">75</a><a href="/search?q=%7B%22source%22%3A%22nominations%22%2C%22congress%22%3A%22114%22%7D&amp;pageSort=actionDesc&amp;pageSize=25&amp;page=76">76</a><a href="/search?q=%7B%22source%22%3A%22nominations%22%2C%22congress%22%3A%22114%22%7D&amp;pageSort=actionDesc&amp;pageSize=25&amp;page=77">77</a><span class="selected" aria-label="Page 78">78</span><span class="next off" aria-hidden="true" aria-label="Next Page"><i></i></span><span class="skip-ahead off" aria-hidden="true" aria-label="Skip Ahead Five Pages"><i></i></span><span class="last off" aria-hidden="true" aria-label="Last Page"><i></i></span></div>
            </div>
        </div>
        """
        expected = False

        result = nominations.next_page_exists(html)
        self.assertEqual(expected, result)

    def test_parse_nomination_ids(self):
        # TODO
        pass

