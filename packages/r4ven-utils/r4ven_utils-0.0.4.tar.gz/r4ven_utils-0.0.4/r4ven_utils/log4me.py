"""
Script that contains all functions related to project logs.
"""

import os
import glob
import inspect
import logging

def function_logger(script_name: str,
                    file_mode: str = "w",
                    file_level: int = logging.INFO,
                    console_level: int = None) -> logging.Logger:
    """
    Creates a log object specific to the function in which it is called.

    Args:
        file_mode (str): A string that defines in which mode the log file will be opened.
        Default: "w" (Write) - Opens a file for writing, creates the file if it doesn't exist.

        file_level (int): Level of log messages that will be written to the log file.
        Default: logging.INFO.

        console_level (int, optional): Level of log messages that will be displayed on the terminal.
        Default: None.

    returns:
        logging.Logger: Log object of the function in which this function is being called.
    """
    create_logs_folder()
    create_script_logs_folder(script_name)

    function_name = inspect.stack()[1][3]
    logger = logging.getLogger(function_name)

    # Check if the log handlers are already running, if so, clean them.
    if (logger.hasHandlers()):
        logger.handlers.clear()

    # By default, log all message levels.
    logger.setLevel(logging.DEBUG)

    if console_level != None:
        # StreamHandler for logs that will be displayed in the terminal.
        ch = logging.StreamHandler()
        ch.setLevel(console_level)
        ch_format = logging.Formatter("%(asctime)s - %(levelname)-8s - %(message)s")
        ch.setFormatter(ch_format)
        logger.addHandler(ch)

    # FileHandler of logs that will be stored in log files.
    fh = logging.FileHandler(r"logs/{0}/{1}.log".\
        format(script_name, function_name), mode = file_mode)
    fh.setLevel(file_level)
    fh_format = logging.\
        Formatter("%(asctime)s - %(levelname)-8s - %(message)s")
    fh.setFormatter(fh_format)
    logger.addHandler(fh)

    return logger

def create_logs_folder() -> None:
    """
    Checks if there is a folder called "logs" in the current directory, if it doesn't exist,
    create this one.
    """
    project_directory = os.getcwd()
    logs_directory = os.path.join(project_directory, "logs")
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

def create_script_logs_folder(script_name: str) -> None:
    """
    Checks if there is a logs folder for the script that is running in the project directory
    (/logs/script_name), if it does not exist, create it.

    Args:
        script_name(str): Name of the script that is calling the function_logger function.
    """
    project_directory = os.getcwd()
    script_logs_directory = project_directory + "/logs"
    final_directory = os.path.join(script_logs_directory, script_name)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

def create_output_logs_folder() -> None:
    """
    Checks if there is a output logs folder in the project directory
    (/logs/output_logs), if it does not exist, create it.
    """
    project_directory = os.getcwd()
    logs_directory = project_directory + "/logs"
    final_directory = os.path.join(logs_directory, "output_logs")
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

def merge_log_files(log_folder_path: str,
                    output_log_path: str,
                    log_files_pattern: str = "*.log") -> None:
    """
    Merges multiple log files from a specified folder into a single log file.

    Args:
        log_folder_path (str): The folder containing the .log files
        output_log_path (str): The output file path for the merged log
        log_files_pattern (str, optional): The pattern for .log files (adjust if needed)
            Defaults to "*.log".
    """

    create_output_logs_folder()

    # Get a list of all .log files in the folder sorted by modification time
    log_files = sorted(glob.glob(os.path.join(log_folder_path, log_files_pattern)), key=os.path.getmtime)

    # Merge the content of all log files into a new file
    with open(output_log_path, "w") as merged_log:
        for log_file in log_files:
            with open(log_file, "r") as current_log:
                merged_log.write(current_log.read())

    print(f"Merged log files written to {output_log_path}")