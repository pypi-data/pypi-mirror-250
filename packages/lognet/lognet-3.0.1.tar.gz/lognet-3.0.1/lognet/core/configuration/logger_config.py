from typing import Optional
from lognet.core.configuration import HandlerConfigurator
from lognet.core.domain import LogLevel


class LoggerConfig:
    """
    Configuration class for logger settings.

    This class allows the configuration of various settings for the logger, such as log format,
    minimum log level, and handler configurator.

    Attributes:
        log_format (Optional[str]): The format to use for log messages. Defaults to None.
        min_level (LogLevel): The minimum log level for messages. Defaults to LogLevel.DEBUG.
        handler_configurator (HandlerConfigurator): The handler configurator for log messages.

    Methods:
        __init__(self, log_format: Optional[str] = None, min_level: LogLevel = LogLevel.DEBUG,
                 handler_configurator: HandlerConfigurator = None) -> None:
            Initializes a new instance of the LoggerConfig class.

    """

    def __init__(self, log_format: Optional[str] = None, min_level: LogLevel = LogLevel.DEBUG,
                 handler_configurator: HandlerConfigurator = None) -> None:
        """
        Initializes a new instance of the LoggerConfig class.

        Args:
            log_format (Optional[str]): The format to use for log messages. Defaults to None.
            min_level (LogLevel): The minimum log level for messages. Defaults to LogLevel.DEBUG.
            handler_configurator (HandlerConfigurator): The handler configurator for log messages.
        """
        self.handler_configurator = handler_configurator
        self.log_format = log_format
        self.min_level = min_level
