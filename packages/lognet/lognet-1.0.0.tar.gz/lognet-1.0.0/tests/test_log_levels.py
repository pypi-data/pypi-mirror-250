import unittest
from lognet import Logger, LogLevel


class TestLoggerLevels(unittest.TestCase):

    def test_debug_level(self):
        logger = Logger(min_level=LogLevel.DEBUG)
        self.assertEqual(logger.min_level, LogLevel.DEBUG, "min_level should be set to DEBUG")

    def test_info_level(self):
        logger = Logger(min_level=LogLevel.INFO)
        self.assertEqual(logger.min_level, LogLevel.INFO, "min_level should be set to INFO")

    def test_warning_level(self):
        logger = Logger(min_level=LogLevel.WARNING)
        self.assertEqual(logger.min_level, LogLevel.WARNING, "min_level should be set to WARNING")

    def test_error_level(self):
        logger = Logger(min_level=LogLevel.ERROR)
        self.assertEqual(logger.min_level, LogLevel.ERROR, "min_level should be set to ERROR")

    def test_critical_level(self):
        logger = Logger(min_level=LogLevel.CRITICAL)
        self.assertEqual(logger.min_level, LogLevel.CRITICAL, "min_level should be set to CRITICAL")


if __name__ == "__main__":
    unittest.main()
