from unittest import TestCase
import wikipedia_names_search


class TestWikipediaNamesSearch(TestCase):

    def setUp(self):
        self.sut = wikipedia_names_search.WikipediaNamesSearch()

    def tearDown(self):
        self.sut = None

    def test__create_url_01(self):
        url = self.sut._WikipediaNamesSearch__create_url("Log Horizon")
        self.assertEqual("https://en.wikipedia.org/wiki/Special:Search/Log_Horizon", url)

    def test_load_page_01(self):
        page = self.sut._WikipediaNamesSearch__load_page("https://en.wikipedia.org/wiki/Special:Search/Log_Horizon")
        pass

    # def test_search_episodes_01(self):
    #     self.fail()
