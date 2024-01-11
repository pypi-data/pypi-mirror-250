import unittest
from lognet import Logger, ConsoleHandler


class TestSingletonLogger(unittest.TestCase):
    def test_singleton_instance(self):
        # Create two logger instances
        logger1 = Logger(console_log_handler=ConsoleHandler())
        logger2 = Logger(console_log_handler=ConsoleHandler())

        # Check that both instances are the same object
        self.assertIs(logger1, logger2)

    def test_singleton_behavior(self):
        # Create multiple logger instances in different scopes
        logger_outer = Logger(console_log_handler=ConsoleHandler())

        def create_inner_logger():
            # Inside a function, create a logger
            logger_inner = Logger(console_log_handler=ConsoleHandler())
            return logger_inner

        logger_inner = create_inner_logger()

        # Check that all instances refer to the same object
        self.assertIs(logger_outer, logger_inner)

    def test_singleton_multiple_instantiations(self):
        # Attempt to instantiate the logger multiple times
        logger1 = Logger(console_log_handler=ConsoleHandler())
        logger2 = Logger(console_log_handler=ConsoleHandler())

        # Check that subsequent instantiations return the same instance
        self.assertIs(logger1, logger2)


if __name__ == "__main__":
    unittest.main()
