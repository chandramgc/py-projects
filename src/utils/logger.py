"""
Module: logger
This module sets up logging for the application. It writes logs both to the console and to a log file.
When the log file reaches 10 KB, it rotates and compresses the older logs.
"""

import logging
import logging.handlers
import os
import zipfile
import datetime
from src.utils.config_reader import ConfigReader


class ZippedRotatingFileHandler(logging.handlers.RotatingFileHandler):
    """
    A RotatingFileHandler that compresses the rotated log files.
    """

    def doRollover(self):
        """
        Performs log rollover and compresses the rotated log file.
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        if self.backupCount > 0:
            for i in range(self.backupCount - 1, 0, -1):
                sfn = f"{self.baseFilename}.{i}"
                dfn = f"{self.baseFilename}.{i + 1}"
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = self.baseFilename + ".1"
            if os.path.exists(dfn):
                os.remove(dfn)
            os.rename(self.baseFilename, dfn)

            # Generate timestamp and create zip filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_filename = f"{dfn}_{timestamp}.zip"

            # Compress the rotated log file into a zip archive
            with zipfile.ZipFile(
                    zip_filename, "w", compression=zipfile.ZIP_DEFLATED
            ) as zipf:
                zipf.write(dfn, arcname=os.path.basename(dfn))
            os.remove(dfn)

        # Reopen the log file
        self.mode = "w"
        self.stream = self._open()


def setup_logger(env="dev"):
    """
    Configures the root logger to output messages both to the console and to a rotating log file.
    The log file rotates after reaching 10 KB, and older logs are compressed.

    Returns:
        logger (logging.Logger): The configured logger.
    """
    # Read configuration from YAML
    config = ConfigReader(env=env)
    log_file = config.get("logging.log_file", "app.log")
    log_level = config.get("logging.level", "DEBUG")
    max_bytes = config.get("logging.max_bytes", 10000)  # 10 KB
    backup_count = config.get("logging.backup_count", 5)  # 5 backups
    # Convert log level string to actual logging level constant
    level = getattr(logging, log_level.upper(), logging.DEBUG)
    log_format = config.get(
        "logging.log_format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Ensure the directory for the log file exists.
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(log_format)

    # Console handler: outputs logs to the terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler: writes logs to a file with rotation at 10 KB and 5 backups
    file_handler = ZippedRotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
