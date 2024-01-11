import functools
import os
import uuid
import weakref
from typing import Optional

import requests
from langsmith import client
from requests import adapters as requests_adapters
from urllib3.util import Retry

from xleap.config import Keys


class L(client.Client):
    def __init__(
        self,
        api_url: Optional[str] = None,
        *,
        api_key: Optional[str] = None,
        retry_config: Optional[Retry] = None,
        timeout_ms: Optional[int] = None,
        web_url: Optional[str] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        """Initialize a Client instance.

        Parameters
        ----------
        api_url : str or None, default=None
            URL for the XLeap API. Defaults to the XLEAP_ENDPOINT
            environment variable or http://localhost:1984 if not set.
        api_key : str or None, default=None
            API key for the XLeap API. Defaults to the XLEAP_API_KEY
            environment variable.
        retry_config : Retry or None, default=None
            Retry configuration for the HTTPAdapter.
        timeout_ms : int or None, default=None
            Timeout in milliseconds for the HTTPAdapter.
        web_url : str or None, default=None
            URL for the XLeap web app. Default is auto-inferred from
            the ENDPOINT.
        session: requests.Session or None, default=None
            The session to use for requests. If None, a new session will be
            created.

        Raises
        ------
        LangSmithUserError
            If the API key is not provided when using the hosted service.
        """
        self.api_key = api_key or os.getenv(Keys.API_KEY.value)
        self.api_url = api_url or os.getenv(Keys.API_ENDPOINT.value)

        self.retry_config = retry_config or client._default_retry_config()
        self.timeout_ms = timeout_ms or 7000
        self._web_url = web_url
        self._tenant_id: Optional[uuid.UUID] = None
        # Create a session and register a finalizer to close it
        self.session = session if session else requests.Session()
        weakref.finalize(self, client.close_session, self.session)

        # Mount the HTTPAdapter with the retry configuration
        adapter = requests_adapters.HTTPAdapter(max_retries=self.retry_config)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self._get_data_type_cached = functools.lru_cache(maxsize=10)(
            self._get_data_type
        )
