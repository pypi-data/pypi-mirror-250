from datetime import datetime
from lognet.core.application.formatters import LogFormatter
from lognet.core.configuration import LoggerConfig
from lognet.core.domain import LogLevel, LogEntity


class Logger:
    """
    Logger class for handling and recording log messages.

    This class is responsible for creating log entities and handling them based on the provided
    configuration. It checks the log level before processing and sends log messages to configured
    handlers, such as console and file handlers.

    Attributes:
        config (LoggerConfig): The configuration for the logger.

    Methods:
        log(self, level: LogLevel, message: str) -> None:
            Logs a message with the specified log level.

    """

    def __init__(self, config: LoggerConfig) -> None:
        """
        Initializes a new instance of the Logger class.

        Args:
            config (LoggerConfig): The configuration for the logger.
        """
        self.config = config

    def log(self, level: LogLevel, message: str) -> None:
        """
        Logs a message with the specified log level.

        This method creates a log entity, checks if the log level is above the minimum level
        configured for the logger, and then sends the log entity to configured handlers.

        Args:
            level (LogLevel): The log level of the message.
            message (str): The log message.

        Returns:
            None
        """
        log_entity = LogEntity(level=level, message=message)
        log_entity.time = datetime.now()

        if log_entity.level.value >= self.config.min_level.value:
            if self.config.handler_configurator:
                console_handler = self.config.handler_configurator.console_handler
                file_handler = self.config.handler_configurator.file_handler

                if console_handler:
                    console_handler.emit(log_entity, LogFormatter.format_message(log_entity, self.config))

                if file_handler:
                    file_handler.emit(log_entity, LogFormatter.format_message(log_entity, self.config))
