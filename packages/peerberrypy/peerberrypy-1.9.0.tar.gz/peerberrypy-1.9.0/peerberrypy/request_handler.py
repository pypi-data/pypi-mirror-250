from peerberrypy.exceptions import PeerberryException
from peerberrypy.constants import CONSTANTS
from typing import Type
import cloudscraper


class RequestHandler:
    def __init__(self, request_params: dict):
        """ Request handler for internal use with Peerberry's specifications. """
        self.__session = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True,
            }
        )
        self._request_params = request_params

    def request(
            self,
            url: str,
            method: str = 'GET',
            exception_type: Type[Exception] = PeerberryException,
            output_type: str = 'json',
            **kwargs,
    ) -> any:
        output_types = CONSTANTS.OUTPUT_TYPES
        output_type = output_type.lower()

        if output_type not in output_types:
            raise ValueError(f'Output type must be one of the following: {", ".join(output_types)}')

        requests_params = self._request_params.copy()
        requests_params.update(kwargs)

        response = self.__session.request(
            method=method,
            url=url,
            **requests_params,
        )

        if response.status_code >= 400:
            if 'application/json' not in response.headers['Content-Type']:
                raise PeerberryException('Unexpected server response')

            error_response = response.json()

            errors = error_response.get('errors')

            if not errors:
                raise exception_type(error_response['message'])

            error_response = errors

            if isinstance(error_response, list):
                raise exception_type(list(error_response[0].values())[0])

            raise exception_type(list(error_response.values())[0])

        if output_type == 'bytes':
            parsed_response = response.content

        else:
            import decimal
            import json
            parsed_response = json.loads(response.text, parse_float=decimal.Decimal)

        return parsed_response

    def get_headers(self) -> object:
        return self.__session.headers

    def add_header(self, header: dict) -> object:
        self.__session.headers.update(header)

        return self.get_headers()

    def remove_header(self, key: str) -> object:
        self.__session.headers.pop(key, None)

        return self.get_headers()
