from lognet import LoggerConfig


class LogFormatter:
    """A utility class for formatting log messages."""

    @staticmethod
    def format_message(log_entity: 'LogEntity', config: LoggerConfig) -> str:
        """
        Format a log message based on the provided log entity and logger configuration.

        Args:
            log_entity ('LogEntity'): The log entity containing information about the log message.
            config ('LoggerConfig'): The logger configuration specifying the log message format.

        Returns:
            str: The formatted log message.
        """
        log_format = config.log_format or "[{time}] [{log_level}] {message}"
        return log_format.format(
            time=log_entity.time,
            log_level=log_entity.level.name,
            message=log_entity.message
        )
