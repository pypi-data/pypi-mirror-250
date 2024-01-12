from enum import Enum


class LogLevel(Enum):
    """
    Enumeration representing different log levels.

    This enumeration defines several log levels with associated numeric values.
    Log levels are used to categorize log entries based on their severity.

    Enum Values:
        DEBUG (int): Debugging information.
        INFO (int): General information.
        WARNING (int): Warning messages.
        ERROR (int): Error messages.
        CRITICAL (int): Critical error messages.

    Example:
        log_level = LogLevel. DEBUG
        print(log_level.value)  # Output: 100

    """
    DEBUG = 100
    INFO = 200
    WARNING = 300
    ERROR = 400
    CRITICAL = 500


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
