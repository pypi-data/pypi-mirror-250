"""Python client for Epion API."""


class EpionAuthenticationError(Exception):
    """Authentication exception."""


class EpionConnectionError(Exception):
    """Connection problem, can be retried."""
