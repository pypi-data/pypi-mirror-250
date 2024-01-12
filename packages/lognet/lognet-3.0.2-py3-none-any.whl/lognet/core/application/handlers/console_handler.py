from lognet.core.domain import LogEntity
from lognet.core.application.handlers.handler import Handler


class ConsoleHandler(Handler):
    """
    Log handler for printing log messages to the console.

    This class inherits from the abstract 'Handler' class and implements the 'emit' method
    for handling and printing log messages to the console.

    Methods:
        emit(self, log_entity: 'LogEntity', log_format: str) -> None:
            Handles and prints a log message to the console.

    """

    def emit(self, log_entity: 'LogEntity', log_format: str) -> None:
        """
        Handles and prints a log message to the console.

        Args:
            log_entity ('LogEntity'): The log entity containing information about the log message.
            log_format (str): The format string for the log message.

        Returns:
            None
        """
        formatted_message = log_format.format(
            time=log_entity.time,
            log_level=log_entity.level.name,
            message=log_entity.message
        )
        print(formatted_message)
