import unittest
from auro_utils.loggers.logger_classic import Logger


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger(console_log_level="debug", use_file_log=False)

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

    def test_singleton_pattern(self):
        try:
            logger_singleton_pattern_test = Logger(
                console_log_level="warning", use_file_log=False)
            logger_singleton_pattern_test.log_debug(
                "test_debug for singleton pattern")
            logger_singleton_pattern_test.log_info(
                "test_info for singleton pattern")
            logger_singleton_pattern_test.log_warning(
                "test_warning for singleton pattern")
            logger_singleton_pattern_test.log_error(
                "test_error for singleton pattern")
            logger_singleton_pattern_test.log_critical(
                "test_critical for singleton pattern")
        except Exception as e:
            self.fail(f"test_singleton_pattern failed with {e}")


if __name__ == "__main__":
    unittest.main()
