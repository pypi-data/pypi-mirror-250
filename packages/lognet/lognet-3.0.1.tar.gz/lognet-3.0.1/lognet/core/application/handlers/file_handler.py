import os
from lognet.core.application.handlers.handler import Handler


class FileHandler(Handler):
    """
    Log handler for writing log messages to a file.

    This class inherits from the abstract 'Handler' class and implements the 'emit' method
    for handling and writing log messages to a file.

    Args:
        file_name (str): The name of the log file.
        mode (str): The file mode (default is 'a' for append).
        max_size (int): The maximum size of the log file in bytes before rotating (default is 1 MB).

    Attributes:
        file_name (str): The name of the log file.
        mode (str): The file mode.
        max_size (int): The maximum size of the log file.
        file (File): The file object for writing log messages.

    Methods:
        __init__(self, file_name: str, mode: str = "a", max_size: int = 1024 * 1024) -> None:
            Constructor to initialize the FileHandler instance.

        __del__(self):
            Destructor to close the file when the FileHandler instance is deleted.

        _get_file_size(self) -> int:
            Returns the size of the log file in bytes.

        _rotate_log(self) -> None:
            Rotates the log file by creating a backup copy and starting a new log file.

        emit(self, log_entity: 'LogEntity', log_format: str) -> None:
            Handles and writes a log message to the file.

    """

    def __init__(self, file_name: str, mode: str = "a", max_size: int = 1024 * 1024) -> None:
        """
        Constructor to initialize the FileHandler instance.

        Args:
            file_name (str): The name of the log file.
            mode (str): The file mode (default is 'a' for append).
            max_size (int): The maximum size of the log file in bytes before rotating (default is 1 MB).

        Returns:
            None
        """
        self.file_name = file_name
        self.mode = mode
        self.max_size = max_size
        self.file = open(self.file_name, self.mode) if file_name else None

    def __del__(self):
        """
        Destructor to close the file when the FileHandler instance is deleted.

        Returns:
            None
        """
        self.file.close()

    def _get_file_size(self) -> int:
        """
        Returns the size of the log file in bytes.

        Returns:
            int: The size of the log file.
        """
        if self.file_name:
            return os.path.getsize(self.file_name)
        return 0

    def _rotate_log(self) -> None:
        """
        Rotates the log file by creating a backup copy and starting a new log file.

        Returns:
            None
        """
        backup_file_name = f"{self.file_name}.bak"
        os.rename(self.file_name, backup_file_name)
        self.file.close()
        self.file = open(self.file_name, self.mode)

    def emit(self, log_entity: 'LogEntity', log_format: str) -> None:
        """
        Handles and writes a log message to the file.

        Args:
            log_entity ('LogEntity'): The log entity containing information about the log message.
            log_format (str): The format string for the log message.

        Returns:
            None
        """
        if self._get_file_size() > self.max_size:
            self._rotate_log()

        formatted_message = log_format.format(
            time=log_entity.time,
            log_level=log_entity.level.name,
            message=log_entity.message
        )
        self.file.write(formatted_message + '\n')
        self.file.flush()
