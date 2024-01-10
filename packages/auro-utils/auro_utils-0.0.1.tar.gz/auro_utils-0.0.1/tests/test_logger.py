import unittest
from unittest.mock import patch
from auro_utils.loggers.logger import Logger


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger(console_log_level="debug", use_file_log=False)

    def test_log_trace(self):
        try:
            self.logger.log_trace("This is a trace message.")
        except Exception as e:
            self.fail(f"test_log_trace failed with {e}")

    def test_log_debug(self):
        try:
            self.logger.log_debug("This is a debug message.")
        except Exception as e:
            self.fail(f"test_log_debug failed with {e}")

    def test_log_info(self):
        try:
            self.logger.log_info("This is an info message.")
        except Exception as e:
            self.fail(f"test_log_info failed with {e}")

    def test_log_success(self):
        try:
            self.logger.log_success("This is a success message.")
        except Exception as e:
            self.fail(f"test_log_success failed with {e}")

    def test_log_warning(self):
        try:
            self.logger.log_warning("This is a warning message.")
        except Exception as e:
            self.fail(f"test_log_warning failed with {e}")

    def test_log_error(self):
        try:
            self.logger.log_error("This is an error message.")
        except Exception as e:
            self.fail(f"test_log_error failed with {e}")

    def test_log_critical(self):
        try:
            self.logger.log_critical("This is a critical message.")
        except Exception as e:
            self.fail(f"test_log_critical failed with {e}")

    def test_log_exception(self):
        with patch.object(self.logger, 'log_exception') as mock_log_exception:
            try:
                a = 5
                b = 0
                c = a / b
            except Exception as e:
                self.logger.log_exception(e)
            # Check if log_exception was called once
            self.assertEqual(mock_log_exception.call_count, 1)

    def test_singleton_pattern(self):
        try:
            logger_singleton_pattern_test = Logger(
                console_log_level="warning", use_file_log=False)
            self.assertEqual(self.logger, logger_singleton_pattern_test)
        except Exception as e:
            self.fail(f"test_singleton_pattern failed with {e}")


if __name__ == "__main__":
    unittest.main()
