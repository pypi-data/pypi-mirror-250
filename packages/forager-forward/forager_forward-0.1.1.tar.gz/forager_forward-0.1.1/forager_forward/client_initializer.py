"""Forager client initializer."""
from __future__ import annotations

from typing import Any, Optional

from forager_forward.app_clients.client import Client


class ClientInitializer(object):
    """Singleton class for client initialization and retrieving."""

    _client: Optional[Client] = None

    def __new__(cls, *args: Any, **kwargs: Any) -> ClientInitializer:
        """Create new instance, if it's None, otherwise use earlier created one."""
        if getattr(cls, 'instance', None) is None:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def initialize_client(self, api_key: str) -> None:
        """Initialize client instance."""
        self._client = Client(api_key)

    @property
    def client(self) -> Optional[Client]:
        """Get client instance."""
        return self._client
