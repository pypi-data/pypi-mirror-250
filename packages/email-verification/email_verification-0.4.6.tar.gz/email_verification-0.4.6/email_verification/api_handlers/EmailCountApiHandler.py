"""Email count api handler."""
from typing import Dict

from email_verification.api_handlers.BaseApiHandler import BaseApiHandler


class EmailCountApiHandler(BaseApiHandler):
    """Class for handling email count API endpoint."""

    @property
    def base_url(self) -> str:
        """Return the base url for the API endpoint."""
        return 'https://api.hunter.io/v2/'

    @base_url.setter
    def base_url(self, inserting_base_url: str) -> None:
        """Insert new base url for Email Verification API endpoint."""
        self._base_url = inserting_base_url

    def make_get_request(self, request_params: Dict[str, str]) -> Dict[str, str]:
        """Get the count of emails for the given domain."""
        return self._get(path='email-count', request_params=request_params)
