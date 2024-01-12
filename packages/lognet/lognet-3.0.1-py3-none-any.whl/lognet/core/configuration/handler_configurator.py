from lognet.core.application.handlers import ConsoleHandler, FileHandler


class HandlerConfigurator:
    """
    Configuration class for handling loggers.

    This class allows the configuration of handlers for log messages. It supports configuring both
    a console handler and a file handler.

    Attributes:
        console_handler (ConsoleHandler): The console handler for log messages.
        file_handler (FileHandler): The file handler for log messages.

    Methods:
        __init__(self, console_handler: ConsoleHandler = None, file_handler: FileHandler = None) -> None:
            Initializes a new instance of the HandlerConfigurator class.

    """

    def __init__(self, console_handler: ConsoleHandler = None, file_handler: FileHandler = None) -> None:
        """
        Initializes a new instance of the HandlerConfigurator class.

        Args:
            console_handler (ConsoleHandler): The console handler for log messages.
            file_handler (FileHandler): The file handler for log messages.
        """
        self.console_handler = console_handler
        self.file_handler = file_handler
