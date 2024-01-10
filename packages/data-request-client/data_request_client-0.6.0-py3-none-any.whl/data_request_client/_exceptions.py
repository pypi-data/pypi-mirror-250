class DataRequestClientError(Exception):
    """Base class for exceptions in this module."""

    pass


class DataRequestClientConnectionError(DataRequestClientError):
    """Raised when a connection error occurs."""

    pass
