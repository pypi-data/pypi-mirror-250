from abc import ABC, abstractmethod


class Handler(ABC):
    """
    Abstract base class for log handlers.

    This class defines the interface for log handlers. Subclasses should implement
    the 'emit' method for handling and outputting log messages.
    """

    @abstractmethod
    def emit(self, log_entity: 'LogEntity', log_format: str) -> None:
        """
        Abstract method to handle and output a log message.

        Args:
            log_entity ('LogEntity'): The log entity containing information about the log message.
            log_format (str): The format string for the log message.

        Returns:
            None
        """
        pass
