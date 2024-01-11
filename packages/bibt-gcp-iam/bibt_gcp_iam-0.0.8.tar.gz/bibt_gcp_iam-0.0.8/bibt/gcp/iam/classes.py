import logging

import google.auth.transport.requests
from google.api_core import exceptions as google_exceptions
from google.cloud import iam_credentials
from google.oauth2 import credentials

_LOGGER = logging.getLogger(__name__)


class Client:
    """A credentials client may be used to generate access tokens and credentials object
    compatible with Google APIs.

    :param google.oauth2.credentials.Credentials credentials: A credentials object to
        override the default behavior of attempting to create credentials using the
        inferred gcloud environment. You probably do NOT need to supply this in
        most cases. Defaults to ``None``.
    """

    def __init__(self, credentials=None):
        self._client = iam_credentials.IAMCredentialsClient(credentials=credentials)

    def _ensure_valid_client(self):
        if not self._client._transport._credentials.valid:
            logging.info(
                "Refreshing client credentials, token expired: "
                f"[{self._client._transport._credentials.expiry}]"
            )
            request = google.auth.transport.requests.Request()
            self._client._transport._credentials.refresh(request=request)
            logging.info(
                f"New expiration: [{self._client._transport._credentials.expiry}]"
            )
        return

    def get_access_token(
        self, target_acct, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    ):
        """
        Generates an access token for a target service account which may be used
        to impersonate that service account in API calls. Requires the calling account
        have the "Service Account Token Creator" role on the target account.

        .. code:: python

            from bibt.gcp import iam
            from google.oauth2 import credentials
            def main(event, context):
                client = iam.Client()
                token = client.get_access_token(
                    target_acct="myserviceaccount@myproject.iam.gserviceaccount.com"
                )
                api_creds = credentials.Credentials(token=token)
                storage_client = storage.Client(credentials=api_creds)
                storage_client.get_bucket("mybucket")

        :type target_acct: :py:class:`str`
        :param target_acct: the email address of the account to impersonate.

        :type scopes: :py:class:`list`
        :param scopes: the scopes to request for the token. by default, will be set
            to ``["https://www.googleapis.com/auth/cloud-platform"]`` which
            should be sufficient for most uses cases.

        :rtype: :py:class:`str`
        :returns: an access token with can be used to generate credentials
            for Google APIs.
        """
        # Create credentials for Logging API at the org level
        _LOGGER.info(
            f"Getting access token for account: [{target_acct}] with scope: [{scopes}]"
        )
        self._ensure_valid_client()
        try:
            resp = self._client.generate_access_token(
                name=target_acct,
                scope=scopes,
            )
        except google_exceptions.PermissionDenied as e:
            _LOGGER.critical(
                "Permission denied while attempting to create access token. "
                "Ensure that the account running this function has the "
                '"Service Account Token Creator" '
                f"role on the target account ({target_acct})."
            )
            raise e

        _LOGGER.info("Returning access token.")
        return resp.access_token

    def get_credentials(
        self, target_acct, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    ):
        """
        Generates a credentials object for a target service account which may be used
        to impersonate that service account in API calls. Requires the calling account
        have the "Service Account Token Creator" role on the target account. This
        version takes care of credentials object creation for you.

        .. code:: python

            from bibt.gcp import iam
            from google.oauth2 import credentials
            def main(event, context):
                client = iam.Client()
                api_creds = client.get_credentials(
                    target_acct="myserviceaccount@myproject.iam.gserviceaccount.com"
                )
                storage_client = storage.Client(credentials=api_creds)
                storage_client.get_bucket("mybucket")

        :type target_acct: :py:class:`str`
        :param target_acct: the email address of the account to impersonate.

        :type scopes: :py:class:`list`
        :param scopes: the scopes to request for the token. by default, will be set
            to ``["https://www.googleapis.com/auth/cloud-platform"]`` which
            should be sufficient for most uses cases.

        :rtype: ``google.oauth2.credentials.Credentials``
        :returns: a credentials object with can be used for authentication
            with Google APIs.
        """
        access_token = self.get_access_token(acct=target_acct, scopes=scopes)

        _LOGGER.info("Generating and returning credentials object.")
        return credentials.Credentials(token=access_token)
