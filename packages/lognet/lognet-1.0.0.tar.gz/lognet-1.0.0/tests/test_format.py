import unittest
import os
from lognet import Logger, LogLevel, FileHandler


class TestLoggerOutputToFile(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for recording logs
        self.log_file_name = "test_log.txt"

    def tearDown(self):
        # Delete the temporary file after running tests
        if os.path.exists(self.log_file_name):
            os.remove(self.log_file_name)

    def test_logger_output_to_file(self):
        expected_output = "[DEBUG] Debug message"

        # Create a logger and log the message
        logger = Logger(file_log_handler=FileHandler(log_file_name=self.log_file_name, log_mode='w'),
                        log_format="[{log_level}] {message}")
        logger.log(level=LogLevel.DEBUG, message="Debug message")

        # close file handler
        logger.file_log_handler.file_handler.close()

        # write to file
        with open(self.log_file_name, "r") as file:
            actual_output = file.read()

        # Comparing the actual output with the expected one
        self.assertEqual(actual_output.strip(), expected_output)


if __name__ == "__main__":
    unittest.main()
