#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
# Copyright © 2023 Auromix.                                                   #
#                                                                             #
# Licensed under the Apache License, Version 2.0 (the "License");             #
# You may not use this file except in compliance with the License.            #
# You may obtain a copy of the License at                                     #
#                                                                             #
#     http://www.apache.org/licenses/LICENSE-2.0                              #
#                                                                             #
# Unless required by applicable law or agreed to in writing, software         #
# distributed under the License is distributed on an "AS IS" BASIS,           #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    #
# See the License for the specific language governing permissions and         #
# limitations under the License.                                              #
#                                                                             #
# Description: Loguru logger class for console and file log.                  #
# Author: Herman Ye                                                           #
###############################################################################

"""
This module defines a Logger class that uses the loguru library for logging.
The Logger class is designed as a singleton, meaning only one instance of this class can exist at a time.
The Logger class provides methods for logging at different levels including trace, debug, info, success, warning, error, critical, and exception.
It also supports logging to both the console and a file. The console log level and the use of file logging can be configured during the initialization of the Logger instance.
The Logger class also provides a method to find the package directory of the script that calls the Logger.
"""

import sys
import os
import time
import inspect


class Logger():
    """
    This is a Logger class that utilizes the loguru library for logging. It is designed as a singleton,
    meaning only one instance of this class can exist at a time. This class provides methods for logging
    at different levels including trace, debug, info, success, warning, error, critical, and exception.
    It also supports logging to both the console and a file. The console log level and the use of file
    logging can be configured during the initialization of the Logger instance.

    https://loguru.readthedocs.io/en/stable/
    """
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        # If the class instance is not created, create one
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls)
            return cls._instance
        # If the class instance is already created, return the created one
        else:
            cls._instance.log_warning(
                "Logger already exists!")
            cls._instance.log_info(
                f"Set [console_log_level] to [{cls._instance.console_log_level}]")
            cls._instance.log_info(
                f"Set [use_file_log] to [{cls._instance.use_file_log}]")

            return cls._instance

    def __init__(self, console_log_level="info", use_file_log=True):
        """Init logger.

        Args:
            console_log_level: console log level, should be one of [debug, info, warning, error, critical].
            use_file_log: whether to use file log.

        Returns:
            None

        """
        # If class is already initialized, skip the init
        if Logger._initialized:
            return
        # Init loguru logger
        import loguru
        self._logger = loguru.logger

        # Init default parameters
        self.console_log_level = console_log_level
        self.use_file_log = use_file_log
        self.logger_level = "TRACE"
        self.diagnose = False
        self.backtrace = False
        self.serialize = True
        if self.console_log_level == "trace":
            self.logger_level = "TRACE"
            self.diagnose = True
            self.backtrace = True
        elif self.console_log_level == "debug":
            self.logger_level = "DEBUG"
            self.diagnose = True
            self.backtrace = True
        elif self.console_log_level == "info":
            self.logger_level = "INFO"
            self.backtrace = True
        elif self.console_log_level == "success":
            self.logger_level = "SUCCESS"
            self.backtrace = True
        elif self.console_log_level == "warning":
            self.logger_level = "WARNING"
            self.backtrace = True
        elif self.console_log_level == "error":
            self.logger_level = "ERROR"
            self.backtrace = True
        elif self.console_log_level == "critical":
            self.logger_level = "CRITICAL"
            self.backtrace = True
        else:
            raise ValueError(
                "Console log level should be one of [trace, debug, info, success, warning, error, critical]")

        # Remove default logger
        self._logger.remove(0)
        # Add console logger
        try:
            self._logger.add(
                sink=sys.stdout,
                level=self.logger_level,
                format="<d><green><b>TIME</b> {time:HH:mm:ss.SSS}</green> | <blue><b>LINE</b> {file}:{name}:{module}:{function}:{line}</blue></d>\n<i><level>{level}: {message}</level></i>",
                diagnose=self.diagnose,
                backtrace=self.backtrace,
            )
        except Exception as e:
            print(f"Failed to add console logger: {e}")

        # Add file logger
        if self.use_file_log:
            try:
                # Get caller file
                caller_file = inspect.stack()[1].filename
                caller_file_name = os.path.splitext(
                    os.path.basename(caller_file))[0]
                # Get the directory of the script which calls this function
                script_directory = os.path.dirname(
                    os.path.abspath(caller_file))
                # Get the top-level package directory
                package_directory = self.find_package_directory(
                    script_directory)
                # Get current time
                current_sys_time = time.strftime(
                    "%Y_%m_%d_%H_%M", time.localtime())
                # Generate log file directory
                logs_directory = os.path.join(
                    package_directory, 'logs', current_sys_time)
                # Create file log directory
                if not os.path.exists(logs_directory):
                    os.makedirs(logs_directory)
                # Generate log file name
                file_name = f"{caller_file_name}.log"
                full_path_file_name = os.path.join(logs_directory, file_name)
                # Log
                self._logger.info(
                    f"Log file will be saved to: \n{full_path_file_name}")
                # Add file logger
                self._logger.add(
                    sink=full_path_file_name,
                    level=self.logger_level,
                    format="{level}|{time:YYYY-MM-DD HH:mm:ss.SSS}|{file}:{name}:{module}:{function}:{line}|{message}",
                    serialize=True,
                    diagnose=self.diagnose,
                    backtrace=self.backtrace,
                )
            except Exception as e:
                print(f"Failed to add file logger: {e}")

        Logger._initialized = True
        self.log_info("Logger initialized.")

    def find_package_directory(self, current_directory=os.path.dirname(os.path.abspath(__file__))):
        while True:
            parent_directory = os.path.dirname(current_directory)
            if not os.path.isfile(os.path.join(parent_directory, '__init__.py')):
                return current_directory
            current_directory = parent_directory

    def __repr__(self):
        return f'Logger, console_log_level={self.console_log_level}, use_file_log={self.use_file_log})'

    def log_trace(self, message, *args, **kwargs):
        self._logger.trace(message, *args, **kwargs)

    def log_debug(self, message, *args, **kwargs):
        self._logger.debug(message, *args, **kwargs)

    def log_info(self, message, *args, **kwargs):
        self._logger.info(message, *args, **kwargs)

    def log_success(self, message, *args, **kwargs):
        self._logger.success(message, *args, **kwargs)

    def log_warning(self, message, *args, **kwargs):
        self._logger.warning(message, *args, **kwargs)

    def log_error(self, message,*args, **kwargs):
        self._logger.opt(exception=True).error(message, *args, **kwargs)

    def log_critical(self, message, *args, **kwargs):
        self._logger.opt(exception=True).critical(message, *args, **kwargs)

    def log_exception(self, message, *args, **kwargs):
        self._logger.exception(message, *args, **kwargs)
