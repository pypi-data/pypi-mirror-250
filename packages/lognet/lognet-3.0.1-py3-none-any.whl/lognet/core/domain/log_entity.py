from lognet.core.domain import LogLevel


class LogEntity:
    """
    Represents a log entry with associated information.

    This class holds information about a log entry, including the log level, log message,
    and the timestamp when the log entry was created.

    Attributes:
        level (LogLevel): The log level of the entry.
        message (str): The log message.
        time: The timestamp when the log entry was created.

    Methods:
        __init__(self, level: LogLevel, message: str):
            Initializes a new instance of the LogEntity class.

    """

    def __init__(self, level: LogLevel, message: str):
        """
        Initializes a new instance of the LogEntity class.

        Args:
            level (LogLevel): The log level of the entry.
            message (str): The log message.
        """
        self.time = None
        self.level = level
        self.message = message
