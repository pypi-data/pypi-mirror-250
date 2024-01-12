import unittest
import sys
from unittest.mock import patch, Mock
from serpentscribe.logger import Logger, log_output


class TestLogger(unittest.TestCase):
    @patch("logging.getLogger")
    @patch("logging.StreamHandler")
    def test_logger_init_stdout(self, mock_stream_handler, mock_get_logger):
        logger = Logger("info")
        _ = (
            logger.logger
        )  # Accessing the logger attribute to trigger the call to getLogger
        mock_get_logger.assert_called_once()

    @patch("logging.getLogger")
    @patch("logging.FileHandler")
    def test_logger_init_file(self, mock_file_handler, mock_get_logger):
        logger = Logger("info", "./logfile")
        _ = (
            logger.logger
        )  # Accessing the logger attribute to trigger the call to getLogger
        mock_get_logger.assert_called_once()


    @patch.object(Logger, "logger")
    def test_log_debug(self, mock_logger):
        logger = Logger("DEBUG")
        logger.log("test_func", (1, 2), {"param": "value"}, "Expected Result")
        mock_logger.debug.assert_called_once()

    @patch.object(Logger, "logger")
    def test_log_info(self, mock_logger):
        logger = Logger("INFO")
        logger.log("test_func", (1, 2), {"param": "value"}, "Expected Result")
        mock_logger.info.assert_called_once()


class TestLogOutputDecorator(unittest.TestCase):
    @patch.object(Logger, "log")
    def test_log_output(self, mock_log):
        @log_output("DEBUG")
        def test_func(x, y, param="value"):
            return "Expected Result"

        result = test_func(1, 2, param="value")
        self.assertEqual(result, "Expected Result")
        mock_log.assert_called_with(
            "test_func", (1, 2), {"param": "value"}, "Expected Result"
        )


if __name__ == "__main__":
    unittest.main()
