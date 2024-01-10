"""Base api handler to build all other handlers for endpoints."""
import logging
from abc import ABC, abstractmethod
from typing import Dict
from urllib.parse import urlencode, urljoin

from requests import Request, Response, Session

logger = logging.getLogger(__name__)


class BaseApiHandler(ABC):
    """Base class for API handlers."""

    def __init__(self, api_key: str) -> None:
        """Initialize the api handler."""
        self.api_key = api_key

    @property
    @abstractmethod
    def base_url(self) -> str:
        """Abstract property to get the base URL if needed."""

    @base_url.setter
    @abstractmethod
    def base_url(self, inserting_base_url: str) -> None:
        """Abstract property to set the base URL."""

    _base_url = None
    session = Session()

    def _make_request(
        self,
        api_path: str,
        custom_base: str = None,
        **kwargs,
    ) -> Dict[str, str]:
        """Protected method to use for making all types of requests."""
        request_url = self._build_url(api_path, kwargs.get('params'), custom_base)
        request = Request(
            method=kwargs.get('method', 'GET'),
            url=request_url,
            headers=kwargs.get('headers', {}),
            data=kwargs.get('data', {}),
        ).prepare()

        try:
            response = self.session.send(request)
        except Exception as exception_error:
            logger.error('Api connection error: {0}'.format(exception_error))
            raise ConnectionError('Api connection error: {0}'.format(exception_error))

        return response.json()

    @staticmethod
    def check_response(response: Response) -> Dict[str, str]:
        """Get response error."""
        response.raise_for_status()
        return response.json()

    def _build_url(self, api_path: str, request_params: Dict[str, str], custom_base: str = None) -> str:
        """Build the full URL."""
        base_url = custom_base or self.base_url
        full_url = urljoin(base_url, api_path)
        if request_params:
            request_params.update({'api_key': self.api_key})
            encoded_params = urlencode(request_params)
            full_url = urljoin(base_url, '{0}?{1}'.format(api_path, encoded_params))
        return full_url

    def _get(
        self,
        path: str,
        request_params: Dict[str, str] = None,
    ) -> Dict[str, str]:
        return self._make_request(
            api_path=path,
            method='GET',
            params=request_params,
        )

    def _post(
        self,
        api_path: str,
        request_data: Dict[str, str] = None,
    ) -> Dict[str, str]:
        return self._make_request(
            api_path=api_path,
            method='POST',
            data=request_data,
        )

    def _put(
        self,
        path: str,
        request_data: Dict[str, str] = None,
    ) -> Dict[str, str]:
        return self._make_request(
            api_path=path,
            method='PUT',
            data=request_data,
        )

    def _patch(
        self,
        path: str,
        request_data: Dict[str, str] = None,
    ) -> Dict:
        return self._make_request(
            path=path,
            method='PATCH',
            data=request_data,
        )

    def _delete(
        self,
        path: str,
        request_params: Dict[str, str] = None,
    ) -> Dict[str, str]:
        return self._make_request(
            api_path=path,
            method='DELETE',
            params=request_params,
        )
