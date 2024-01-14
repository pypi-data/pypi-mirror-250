"""
test_cryptocurrencies.py This file contains the integration tests for the
cryptocurrencies endpoints.
"""

from unittest import TestCase

from cryptopi import CoinMarketCapApi
from cryptopi.models import Symbol
from cryptopi.utils import find_api_key

# Load the API Key from env.
API_KEY = find_api_key()


class TestCryptoCurrencies(TestCase):
    def __init__(self, *args, **kwargs):
        """
        Initializes the ``TestCryptoCurrencies`` instance.
        :param args: The arguments.
        :param kwargs: The keyword arguments.
        """

        super().__init__(*args, **kwargs)
        self._api = CoinMarketCapApi(api_key=API_KEY, sandbox=False)

    def test_map(self):
        """
        Test the `/cryptocurrency/map` endpoint.
        :return:
        """

        # Request only BTC and ETH.
        params = {"symbol": [Symbol.BTC, Symbol.ETH]}
        map_response = self._api.cryptocurrency_map(**params)

        self.assertIsNotNone(map_response)
        self.assertIsNotNone(map_response.status)
        self.assertIsNotNone(map_response.data)
        self.assertTrue(len(map_response.data) == 2)

    def test_latest_listings(self):
        """
        Test the `/cryptocurrency/listings/latest` endpoint.
        :return:
        """

        # Request only BTC and ETH.
        params = {"limit": 5}
        listings_response = self._api.cryptocurrency_latest_listings(**params)

        self.assertIsNotNone(listings_response)
        self.assertIsNotNone(listings_response.status)
        self.assertIsNotNone(listings_response.data)
        self.assertTrue(len(listings_response.data) == 5)

    def test_latest_quotes(self):
        """
        Test the `/cryptocurrency/quotes/latest` endpoint.
        :return:
        """

        # Request only BTC and ETH.
        params = {"symbol": [Symbol.BTC, Symbol.ETH]}
        quotes_response = self._api.cryptocurrency_latest_quotes(**params)

        self.assertIsNotNone(quotes_response)
        self.assertIsNotNone(quotes_response.status)
        self.assertIsNotNone(quotes_response.data)
        self.assertTrue(len(quotes_response.data) == 2)

        # Request default symbols.
        params = {}
        quotes_response = self._api.cryptocurrency_latest_quotes(**params)

        self.assertIsNotNone(quotes_response)
