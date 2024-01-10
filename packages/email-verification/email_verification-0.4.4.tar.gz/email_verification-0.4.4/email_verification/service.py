"""Service to use email verification client with database."""
import logging
from typing import Dict, List, Tuple

from email_verification.api_handlers.EmailCountApiClient import EmailCountApiClient
from email_verification.api_handlers.EmailVerifierApiClient import EmailVerifier
from email_verification.database import ResultDatabase
from email_verification.utils.response_normilizer import response_normalizer


class EmailVerificationService(object):
    """Email verification service."""

    def __init__(self, api_key: str, db: ResultDatabase) -> None:
        """Initialize the service."""
        self.count_client = EmailCountApiClient(api_key)
        self.verify_client = EmailVerifier(api_key)
        self.db = db
        self.logger = logging.getLogger(__name__)

    def count_emails(self, domain: str, **kwargs: str) -> Dict[str, str]:
        """Count the number of emails in the given domain and handle errors."""
        try:
            return self.count_client.get_email_count({'domain': domain, **kwargs})
        except Exception as exception:
            self.logger.error(
                'Error counting emails for domain {0}: {1}'.format(domain, exception),
            )
            return {'Error': 'Counting emails error: {0}'.format(str(exception))}

    def email_verification(self, email: str) -> Dict[str, str]:
        """Email verification using hunter client and database."""
        try:
            verification_result = self.verify_client.verify_email(email)
        except Exception as exception:
            self.logger.error(
                'Error verifying email {0}: {1}'.format(email, exception),
            )
            return {'Error': 'Verification error: {0}'.format(str(exception))}

        if not verification_result.get('errors'):
            verification_result = response_normalizer(verification_result)
            email_to_save = verification_result.pop('meta_params_email')
            self.db.create_result(email_to_save, verification_result)
            return verification_result
        return verification_result

    def get_all_results(self) -> List[Dict[str, str]]:
        """Show all verification results."""
        return self.db.get_results()

    def delete_result(self, email: str) -> Tuple[str, Dict[str, str]]:
        """Delete result and handle errors."""
        try:
            self.db.delete_result(email)
        except Exception as exception:
            return email, {
                'error': 'Unexpected error: {exception}'.format(
                    exception=str(exception),
                ),
            }
        return email, {'status': 'deleted'}

    def get_result(self, email: str) -> Dict[str, str]:
        """Get verification email if exists."""
        try:
            get_result = self.db.get_result(email)
        except Exception as exception:
            return {
                'error': 'Unexpected error: {exception}'.format(
                    exception=str(exception),
                ),
            }
        return get_result
