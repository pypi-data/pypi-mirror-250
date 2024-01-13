import json

import requests

from .base import FlaskChest


class FlaskChestCustomWriter(FlaskChest):
    """A FlaskChest that writes to a custom endpoint."""

    def __init__(
        self,
        name=None,
        url=None,
        headers=None,
        params=None,
        proxies=None,
        payload_generator=None,
        verify=False,
        success_status_codes=[200],
        logger=None,
    ):
        self.name = name
        self.url = url

        if self.name is None:
            self.name = self.url

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
            "name": self.name,
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
        self.logger.info(f"Writing to FlaskChestCustomWriter(name={self.name})")
        self.logger.debug(f"Writing context tuple list: {context_tuple_list}")

        # Generate the payload, throw an exception if it fails
        try:
            payload = self.payload_generator(context_tuple_list)
        except Exception:
            self.logger.exception(
                f"Error generating payload for FlaskChestCustomWriter(name={self.name})"
            )
            raise Exception(
                f"Error generating payload for FlaskChestCustomWriter(name={self.name})"
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

        self.logger.debug(
            f"Response code from FlaskChestCustomWriter(name={self.name} POST request: {response.status_code}"
        )
        self.logger.debug(
            f"Response from FlaskChestCustomWriter(name={self.name} POST request: {response.text}"
        )

        # If the response status code is in the success status codes, log success
        if response.status_code in self.success_status_codes:
            self.logger.debug(
                f"Successful write to FlaskChestCustomWriter(name={self.name})"
            )
        else:
            self.logger.exception(
                f"Error response code returned when writing to FlaskChestCustomWriter(name={self.name}), {response.status_code} not in success status codes {self.success_status_codes}! {response.text}"
            )
            raise Exception(
                f"Error response code returned when writing to FlaskChestCustomWriter(name={self.name}), {response.status_code} not in success status codes {self.success_status_codes}! {response.text}"
            )
