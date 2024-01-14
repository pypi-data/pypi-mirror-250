"""
definitions.py This file contains API Request classes.
"""
from abc import ABC
from abc import abstractmethod
from http import HTTPMethod

from cmc.api.urls.interface import CryptoCurrencyUrl
from cmc.api.urls.requests.models import CryptoCurrenciesListingParams
from cmc.api.urls.requests.models import CryptoCurrenciesMapParams
from cmc.api.urls.requests.models import CryptoCurrenciesQuoteParams


class Request(ABC):
    """
    The ``Request`` class represents an API request.
    """

    def __init__(self, sandbox: bool = False, **params):
        """
        Initializes the ``Request`` instance.
        :param params: The parameters.
        """

        self._sandbox = sandbox
        self._params = params
        self._interface = None

    @property
    @abstractmethod
    def method(self):
        """
        Return the method.
        :return:
        """

    @property
    @abstractmethod
    def url(self):
        """
        Return the CryptoCurrencyUrl.
        :return:
        """

    @property
    def sandbox(self):
        """
        Return whether the API is for the sandbox.
        :return:
        """

        return self._sandbox

    @property
    def params(self):
        """
        Return the parameters.
        :return:
        """

        return self._params

    @property
    def interface(self):
        """
        Return the interface.
        :return:
        """

        if self._interface is None:
            self._interface = CryptoCurrencyUrl(sandbox=self.sandbox)
        return self._interface


class CryptoCurrenciesMapRequest(Request, ABC):
    """
    The ``CryptoCurrenciesMapRequest`` class represents a request to the
    `/cryptocurrency/map` endpoint.
    """

    def __init__(self, params: CryptoCurrenciesMapParams):
        """
        Initializes the ``CryptoCurrenciesMapRequest`` instance.
        """

        super().__init__(**params.model_dump())

    @property
    def method(self):
        """
        Return the method.
        :return:
        """

        return HTTPMethod.GET

    @property
    def url(self):
        """
        Return the CryptoCurrencyUrl.
        :return:
        """

        return self.interface.map


class CryptoCurrenciesLatestListingsRequest(Request):
    """
    The ``CryptoCurrenciesLatestListingsRequest`` class represents a request to the
    `/cryptocurrency/listings/latest` endpoint.
    """

    def __init__(self, params: CryptoCurrenciesListingParams):
        """
        Initializes the ``CryptoCurrenciesMapRequest`` instance.
        """

        super().__init__(**params.model_dump())

    @property
    def method(self):
        """
        Return the method.
        :return:
        """

        return HTTPMethod.GET

    @property
    def url(self):
        """
        Return the CryptoCurrencyUrl.
        :return:
        """

        return self.interface.latest_listings


class CryptoCurrenciesLatestQuotesRequest(Request):
    """
    The ``CryptoCurrenciesLatestQuotesRequest`` class represents a request to the
    `/cryptocurrency/quotes/latest` endpoint.
    """

    def __init__(self, params: CryptoCurrenciesQuoteParams):
        """
        Initializes the ``CryptoCurrenciesMapRequest`` instance.
        """

        super().__init__(**params.model_dump())

    @property
    def method(self):
        """
        Return the method.
        :return:
        """

        return HTTPMethod.GET

    @property
    def url(self):
        """
        Return the CryptoCurrencyUrl.
        :return:
        """

        return self.interface.latest_quotes
