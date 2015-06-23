from pytt.fetch import SSUFetcher
from django.test import TestCase
import httpretty

class TestFetch(TestCase):

    @httpretty.activate
    def test_correct_simple(self):
        httpretty.register_uri(httpretty.GET,
                               'http://sgu.ru/api',
                               body='<xml>Hello</xml>',
                               content_type='application/xml')

        fetcher = SSUFetcher('sgu.ru/api')
        result = fetcher.fetch_general()
        assert result['success'] == True
        assert result['text'] == '<xml>Hello</xml>'

    @httpretty.activate
    def test_incorrect_simple_excpetion(self):
        httpretty.register_uri(httpretty.GET, 'http://sgu.ru/api',
                               body='',
                               status='501')

        fetcher = SSUFetcher('sgu.ru/api')
        result = fetcher.fetch_general()
        assert result['success'] == False


