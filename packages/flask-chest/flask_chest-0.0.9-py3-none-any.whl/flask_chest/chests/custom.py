import json

import requests

from .base import FlaskChest


class FlaskChestCustomWriter(FlaskChest):
    """Payload generator is must be a function that takes variable_name, variable_value, and request_id as arguments and returns a dictionary
    which will be used as the payload for the POST request to the custom writer"""

    def __init__(
        self,
        url=None,
        headers=None,
        params=None,
        proxies=None,
        payload_generator=None,
        verify=False,
        success_status_codes=[200],
        logger=None,
    ):
        self.url = url
        self.headers = headers
        self.params = params
        self.proxies = proxies
        self.payload_generator = payload_generator
        self.verify = verify
        self.success_status_codes = success_status_codes
        self.logger = logger

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        return {
            "type": "custom_writer",
            "url": self.url,
            "headers": self.headers,
            "params": self.params,
            "proxies": self.proxies,
            "verify": self.verify,
            "success_status_codes": self.success_status_codes,
        }

    def write(
        self,
        context_tuple_list: list,
    ) -> None:
        self.logger.debug("FlaskChestCustomWriter: Writing to custom writer...")
        self.logger.debug(
            f"FlaskChestCustomWriter: Context tuple list: {context_tuple_list}"
        )

        try:
            # Build the payload
            payload = self.payload_generator(context_tuple_list)
        except Exception as e:
            raise Exception(
                f"FlaskChestCustomWriter: Failure! Error generating payload: {e}"
            )

        # Send the POST request
        response = requests.post(
            self.url,
            headers=self.headers,
            params=self.params,
            proxies=self.proxies,
            data=payload,
            verify=self.verify,
        )

        if response.status_code in self.success_status_codes:
            self.logger.debug(
                f"FlaskChestCustomWriter: Success! Status code {response.status_code} received from custom writer! {response.text}"
            )
        else:
            raise Exception(
                f"FlaskChestCustomWriter: Failure! Status code {response.status_code} not in success status codes {self.success_status_codes}! {response.text}"
            )
