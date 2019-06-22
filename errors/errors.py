from discord.ext.commands import CheckFailure


class NotAllowed(CheckFailure):
    """Exception raised when the message author is allowed to use a command.

    This inherits from :exc:`CheckFailure`
    """
    pass


class DateFormatError(Exception):
    """Exception raised when date format is wrong"""
    pass
