"""
api.py This module contains the interface to the CoinMarketCap API.
"""
from http import HTTPMethod
from typing import List

import requests
from cmc.api.urls.data import Symbol
from cmc.api.urls.interface import CryptoCurrencyUrl
from cmc.api.urls.requests.definitions import CryptoCurrenciesLatestListingsRequest
from cmc.api.urls.requests.definitions import CryptoCurrenciesLatestQuotesRequest
from cmc.api.urls.requests.definitions import CryptoCurrenciesMapRequest
from cmc.api.urls.requests.definitions import Request
from cmc.api.urls.requests.models import CryptoCurrenciesListingParams
from cmc.api.urls.requests.models import CryptoCurrenciesMapParams
from cmc.api.urls.requests.models import CryptoCurrenciesQuoteParams
from cmc.api.urls.responses import ListingResponse
from cmc.api.urls.responses import MapResponse
from cmc.api.urls.responses import QuoteResponse


class CoinMarketCapApi:
    """
    The ``CoinMarketCapApi`` class is the interface to the CoinMarketCap API.
    """

    def __init__(self, api_key: str, sandbox: bool = False):
        """
        Initializes the ``CoinMarketCapApi`` instance.
        :param api_key: The API key.
        """

        self._api_key = api_key
        self._sandbox = sandbox
        self._session = None
        self._interface = None

    @property
    def api_key(self):
        """
        Return the API key.
        :return:
        """

        return self._api_key

    @property
    def sandbox(self):
        """
        Return whether the API is for the sandbox.
        :return:
        """

        return self._sandbox

    @property
    def session(self):
        """
        Return the session.
        :return:
        """

        if self._session is None:
            self._session = requests.Session()

        return self._session

    @property
    def headers(self):
        """
        Return the headers.
        :return:
        """

        return {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": self.api_key,
        }

    def _execute_request(self, request: Request) -> dict:
        """
        Execute a request.
        :return:
        """

        # Get the proper method.
        method = {
            HTTPMethod.GET: self._get,
        }[request.method]

        # Execute the request.
        return method(request.url, params=request.params)

    def _get(self, url: str, params: dict = None) -> dict:
        """
        Make a GET request to the API.
        :param url: The CryptoCurrencyUrl.
        :param params: The parameters.
        :return:
        """

        response = self.session.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        return response.json()

    def cryptocurrency_map(self, **params) -> MapResponse:
        """
        Return the cryptocurrency map.
        :return:
        """

        # Apply the parameters.
        params = CryptoCurrenciesMapParams(**params)

        # Build the request.
        request = CryptoCurrenciesMapRequest(params=params)

        # Execute the request.
        response = self._execute_request(request)

        return MapResponse(**response)

    def cryptocurrency_latest_listings(self, **params) -> ListingResponse:
        """
        Return the cryptocurrency listings.
        :return:
        """

        # Apply the parameters.
        params = CryptoCurrenciesListingParams(**params)

        # Build the request.
        request = CryptoCurrenciesLatestListingsRequest(params=params)

        # Execute the request.
        response = self._execute_request(request)

        return ListingResponse(**response)

    def cryptocurrency_latest_quotes(self, **params) -> QuoteResponse:
        """
        Return the cryptocurrency quotes.
        :param params:
        :return:
        """

        # Apply the parameters.
        params = CryptoCurrenciesQuoteParams(**params)

        # Build the request.
        request = CryptoCurrenciesLatestQuotesRequest(params=params)

        # Execute the request.
        response = self._execute_request(request)

        return QuoteResponse(**response)
