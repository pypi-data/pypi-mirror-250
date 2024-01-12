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
        log_level = LogLevel.DEBUG
        print(log_level.value)  # Output: 100

    """
    DEBUG = 100
    INFO = 200
    WARNING = 300
    ERROR = 400
    CRITICAL = 500
