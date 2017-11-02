import lxml
import urllib, urllib2


class WikipediaNamesSearch():
    WIKI_SEARCH_URL="https://en.wikipedia.org/wiki/Special:Search/"

    def __init__(self):
        pass

    @staticmethod
    def __load_page(url):
        response = urllib2.urlopen(url)
        html = response.read()
        return html

    def __create_url(self, series_name):
        series_name = series_name.replace(" ", "_")
        return self.WIKI_SEARCH_URL+str(series_name)

    def search_episodes(self, series_name):
        page = self.__load_page(self.__create_url(series_name))
