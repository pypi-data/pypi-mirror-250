"""Base Api Client Class for hunters."""
from typing import Dict


class ApiClient(object):
    """Base Api class for all handlers."""

    def __init__(self, api_key) -> None:
        """Initialize the ApiClient object."""
        self.handlers: dict = {}
        self.api_key: str = api_key

    def register_client_handler(self, endpoint: str, endpoint_handler: type) -> None:
        """Adding new object to the handlers."""
        self.handlers[endpoint] = endpoint_handler(api_key=self.api_key)

    def make_request(self, endpoint: str, method: str, **kwargs) -> Dict:
        """Make a request to endpoint with the specified method."""
        if endpoint in self.handlers:
            endpoint_handler = self.handlers.get(endpoint)

            # Check if the handler has the specified method
            handler_method = getattr(endpoint_handler, 'make_{0}_request'.format(method.lower()), None)
            if callable(handler_method):
                return handler_method(**kwargs)
            raise AttributeError('Handler {0} does not support {1} requests.'.format(endpoint, method))
        raise ValueError('Invalid endpoint: {0}'.format(endpoint))
