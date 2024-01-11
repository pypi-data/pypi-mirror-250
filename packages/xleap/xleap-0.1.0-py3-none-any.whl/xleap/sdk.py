import logging
import os
from functools import partial

import requests

from xleap.client.api.data import (
    create_rag_data_point,
    destroy_rag_data_point,
    list_rag_data_points,
    retrieve_rag_data_point,
    update_rag_data_point,
)
from xleap.config import Keys
from xleap.utils.login import Auth

logger = logging.getLogger(__name__)


from xleap.client import Client


class Xleap:
    session = requests.Session()

    def __init__(
        self, api_key: str = None, base_url: str = "http://localhost:8000"
    ) -> None:
        self.__api_key = (
            os.getenv(Keys.API_KEY.value) or api_key or self._load_auth_header()
        )
        if not self.__api_key:
            logger.warning("api key not available")

        self.base_url = os.getenv(Keys.API_ENDPOINT.value) or base_url

        self.client = Client(
            self.base_url,
            headers={
                "content-type": "application/json",
                "Authorization": self.__api_key,
            },
        )

    def _load_auth_header(self):
        auth = Auth()
        auth.from_env()
        return auth.auth_header

    @property
    def data(self):
        class Data:
            create = partial(
                create_rag_data_point.sync_detailed, client=self.client
            )
            destroy = partial(
                destroy_rag_data_point.sync_detailed, client=self.client
            )
            retrieve = partial(
                retrieve_rag_data_point.sync_detailed, client=self.client
            )
            update = partial(
                update_rag_data_point.sync_detailed, client=self.client
            )
            list = partial(
                list_rag_data_points.sync_detailed, client=self.client
            )

        return Data()

