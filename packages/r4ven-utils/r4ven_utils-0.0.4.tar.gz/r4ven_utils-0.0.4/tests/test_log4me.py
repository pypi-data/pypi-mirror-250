"""
Test script for my logging related functions.
"""

import os
import sys

# Getting the name of the directory where the this file is present.
current_directory = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name where the current directory is present.
parent_directory = os.path.dirname(current_directory)

# Adding the parent directory to the sys.path.
sys.path.append(parent_directory)

# Import the main function [function_logger()] from function_logger.py
from r4ven_utils.log4me import function_logger

# Get the base name of the script file (excluding the '.py' extension) using os.path.basename
# and remove the '.py' suffix from the obtained base name.
script_name = os.path.basename(__file__).removesuffix(".py")

# Import logging module to get the logging.levels constants.
import logging

def get_logging_levels(file_level: int) -> list:
    """
    Get the list of logging levels that are greater or equal than file_level
    parameter of the function_logger() function.

    Args:
        file_level (int): Logging level that is passed to function_logger()
        as the parameter file_level.

    Returns:
        list: List containing all logging levels names, as strings, that have a priority
        greater or equal to the file_level parameter of the function_logger() function.
    """
    dict_logging_levels = {logging.DEBUG : "DEBUG",
                      logging.INFO : "INFO",
                      logging.WARNING: "WARNING",
                      logging.ERROR : "ERROR",
                      logging.CRITICAL : "CRITICAL"}

    list_logging_levels = []
    for key, value in dict_logging_levels.items():
        if key >= file_level:
            list_logging_levels.append(value)

    return list_logging_levels

def check_file_level(function_name: str, file_level: int) -> None:
    """
    Check if the log file contains the expected logging levels.

    Args:
        function_name (str): The name of the function that's calling the function
        function_logger.
    """
    logs_directory = os.getcwd()
    logs_directory = os.path.join(logs_directory, "logs")
    function_log_path = logs_directory + "/log4me/{}.log".format(function_name)

    # Get file object reference for the file.
    with open (file = function_log_path, mode = "r") as file:
        # Read the content of the file to string.
        file_to_be_inspected = file.read()

        logging_levels = get_logging_levels(file_level)

        if all(logging_level in file_to_be_inspected for logging_level in logging_levels):
            print("For {}: ".format(function_name))
            print("All logging levels with a priority greater or equal" +\
                  " {} are present in the {}.log file. \n".format(file_level, function_name))
        else:
            sys.exit()


def f1() -> None:
    """
    Function that test a specific case of the function_logger(), from src.function_logger.

    Case 01:

        Args:
            > file_level (str): Logging level that will be written in the log file.
                > file_level = None;
                The function should write all logging levels with priority equal or above DEBUG
                to the f1.log file.

            > console_level (str, optional): Logging level that will be displayed
            at the console.
                > console_level = None;
                The function shouldn't write any message to the console, because there isn't any
                logging level assigned to the console_level variable.
    """
    f1_logger = function_logger(script_name = script_name, file_level = logging.DEBUG)
    f1_logger.debug("f1 Debug message")
    f1_logger.info("f1 Information message")
    f1_logger.warning("f1 Warning message")
    f1_logger.error("f1 Error message")
    f1_logger.critical("f1 Critical message")

def f2() -> None:
    """
    Function that test a specific case of the function_logger(), from src.function_logger.

    Case 02:

        Args:
            > file_level (str): Logging level that will be written in the log file.
                > file_level = logging.WARNING;
                The function should write all logging levels with priority equal or above WARNING
                to the f2.log file.

            > console_level (str, optional): Logging level that will be displayed
            at the console.
                > console_level = None;
                The function should write all logging levels with priority equal or above INFO
                to the console.
    """
    f2_logger = function_logger(script_name = script_name,
                                file_mode = "a",
                                file_level = logging.WARNING,
                                console_level = logging.INFO)
    f2_logger.debug("f2 Debug message")
    f2_logger.info("f2 Information message")
    f2_logger.warning("f2 Warning message")
    f2_logger.error("f2 Error message")
    f2_logger.critical("f2 Critical message")

def test_function_logger() -> None:
    """
    Test possible scenarios of the logging function [function_logger()] of the log4me package.
    """
    try:
        f1()
        check_file_level("f1", logging.DEBUG)
        logging.shutdown()
    except SystemExit:
        print()
    try:
        f2()
        check_file_level("f2", logging.WARNING)
        logging.shutdown()
    except SystemExit:
        print()

if __name__ == "__main__":
    test_function_logger()
