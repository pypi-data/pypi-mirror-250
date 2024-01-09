"""Client with base functionality."""
from typing import Any, Optional

import httpx

from forager_forward.common.exceptions import ForagerAPIError


class BaseClient(object):
    """Base functionality for client."""

    def __init__(self, api_key: str) -> None:
        """Initialize client."""
        self.api_key: str = api_key
        self.endpoint: str = 'https://api.hunter.io/v2/'

    def _perform_request(
        self,
        operation: str,
        method: str = 'get',
        raw: bool = False,
        **kwargs: Any,
    ) -> dict | httpx.Response:
        """Perform http request."""
        param_dict: dict = kwargs.get('param_dict', {})
        param_dict['api_key'] = self.api_key
        request = httpx.Request(
            method,
            '{domain}{operation}'.format(domain=self.endpoint, operation=operation),
            params=param_dict,
            json=kwargs.get('payload'),
            headers=kwargs.get('headers'),
        )
        with httpx.Client() as client:
            response: httpx.Response = client.send(request)
        if raw:
            return response
        some_data: Optional[dict] = response.json().get('data')
        if some_data is not None:
            return some_data
        raise ForagerAPIError(response.json())

    async def _aperform_request(
        self,
        operation: str,
        method: str = 'get',
        raw: bool = False,
        **kwargs: Any,
    ) -> dict | httpx.Response:
        """Perform async http request."""
        param_dict: dict = kwargs.get('param_dict', {})
        param_dict['api_key'] = self.api_key
        request = httpx.Request(
            method,
            '{domain}{operation}'.format(domain=self.endpoint, operation=operation),
            params=param_dict,
            json=kwargs.get('payload'),
            headers=kwargs.get('headers'),
        )
        async with httpx.AsyncClient() as client:
            response = await client.send(request)
        if raw:
            return response
        some_data: Optional[dict] = response.json().get('data')
        if some_data is not None:
            return some_data
        raise ForagerAPIError(response.json())
