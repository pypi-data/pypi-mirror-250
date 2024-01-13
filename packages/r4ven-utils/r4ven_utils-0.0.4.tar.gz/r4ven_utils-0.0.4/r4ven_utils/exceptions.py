"""
Library specific exception definitions.
"""

class r4ven_utilsError(Exception):
    """
    Base r4ven_utils exception that all others inherit.
    This is done to not pollute the built-in exceptions, which *could* result
    in unintended errors being unexpectedly and incorrectly handled within
    implementers code.
    """

class TestFailed(r4ven_utilsError):
    """
    Test failed exception.
    """

class MaxRetriesExceeded(r4ven_utilsError):
    """
    Maximum number of retries exceeded.
    """

class HTMLParseError(r4ven_utilsError):
    """
    HTML could not be parsed.
    """

class ExtractError(r4ven_utilsError):
    """
    Data extraction based exception.
    """