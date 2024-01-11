import json
import logging

import google.auth.transport.requests
from google.cloud import secretmanager

_LOGGER = logging.getLogger(__name__)


class Client:
    """A Client object may be used to interact with the GCP secret manager API.

    :param google.oauth2.credentials.Credentials credentials: the credentials
        object to use when making the API call, if not to use the inferred
        gcloud account.
    """

    def __init__(self, credentials=None):
        self._client = secretmanager.SecretManagerServiceClient(credentials=credentials)

    def _ensure_valid_client(self):
        if (
            not self._client._transport._credentials.valid
            or not self._client._transport._credentials.expiry
        ):
            logging.info(
                "Refreshing client credentials, token expired: "
                f"[{str(self._client._transport._credentials.expiry)}]"
            )
            request = google.auth.transport.requests.Request()
            self._client._transport._credentials.refresh(request=request)
            logging.info(
                f"New expiration: [{str(self._client._transport._credentials.expiry)}]"
            )
        else:
            logging.debug(
                f"Token is valid: [{self._client._transport._credentials.valid}] "
                f"expires: [{str(self._client._transport._credentials.expiry)}]"
            )
        return

    def get_secret(
        self,
        host_project,
        secret_name,
        version="latest",
        decode=True,
        parse_json=True,
        timeout=None,
    ):
        """Gets a secret from GCP and returns it either as a dictionary, decoded
            utf-8 string, or raw bytes (depending on the ``parse_json`` and ``decode``
            parameters). Executing account must have (at least) secret version
            accessor permissions on the secret.

        .. code:: python

            from bibt.gcp.secrets import Client
            client = Client()
            secret = client.get_secret(
                "my_project", "my_secret"
            )
            print(secret)

        :type host_project: :py:class:`str`
        :param secret_uri: the project ID of the location of the secret.

        :type secret_name: :py:class:`str`
        :param secret_name: the name of the secret to fetch.

        :type version: :py:class:`str`
        :param version: the version of the secret to fetch. Defaults to ``latest``.

        :type decode: :py:class:`bool`
        :param decode: (Optional) whether or not to decode the bytes into a string.
            Defaults to ``True``.

        :type parse_json: :py:class:`bool`
        :param parse_json: (Optional) whether or not to load the decoded string as
            a JSON object and return a dictionary. Ignored if ``decode==False``.
            Defaults to ``True``.

        :type timeout: :py:class:`float`
        :param timeout: request timeout may be specified if desired.

        :rtype: :py:class:`bytes` OR :py:class:`str`
        :returns: the secret data.
        """
        secret_uri = f"projects/{host_project}/secrets/{secret_name}/versions/{version}"
        _LOGGER.info(f"Fetching secret: [{secret_uri}]")
        _LOGGER.debug(
            f"timeout=[{timeout}] decode=[{decode}] parse_json=[{parse_json}]"
        )
        self._ensure_valid_client()
        secret = self._client.access_secret_version(
            request={"name": secret_uri},
            timeout=timeout,
        ).payload.data
        if decode:
            _LOGGER.debug("Decoding bytes...")
            secret = secret.decode("utf-8")
            if parse_json:
                _LOGGER.debug("Parsing JSON...")
                secret = json.loads(secret)
        _LOGGER.debug("Returning secret...")
        return secret
