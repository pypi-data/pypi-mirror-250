"""Email Verification API Client."""
from typing import Dict

from email_verification.api_handlers.BaseApiHandler import BaseApiHandler


class EmailVerifierApiHandler(BaseApiHandler):
    """Class for handling email verification API endpoint."""

    @property
    def base_url(self) -> str:
        """Base URL for Email Verification API endpoint."""
        return 'https://api.hunter.io/v2/'

    @base_url.setter
    def base_url(self, inserting_base_url: str) -> None:
        """Insert new base url for Email Verification API endpoint."""
        self._base_url = inserting_base_url

    def make_get_request(self, email: str) -> Dict:
        """Verify the given email."""
        return self._get(path='email-verifier', request_params={'email': email})
