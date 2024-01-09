"""Client for Forager project."""
from __future__ import annotations

from forager_forward.app_clients.base import BaseClient
from forager_forward.app_clients.email_client import AsyncEmailClient, EmailClient


class Client(BaseClient, EmailClient, AsyncEmailClient):
    """Base functionality for client."""
