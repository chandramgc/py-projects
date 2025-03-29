import os
import logging
import logging.handlers
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
            # Shift backup files.
            for i in range(self.backupCount - 1, 0, -1):
                sfn = f"{self.baseFilename}.{i}"
                dfn = f"{self.baseFilename}.{i + 1}"
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            # Rotate the current log file.
            dfn = self.baseFilename + ".1"
            if os.path.exists(dfn):
                os.remove(dfn)
            os.rename(self.baseFilename, dfn)

            # Create a ZIP archive of the rotated log file.
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_filename = f"{dfn}_{timestamp}.zip"
            with zipfile.ZipFile(zip_filename, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(dfn, arcname=os.path.basename(dfn))
            os.remove(dfn)

        # Reopen the log file for writing.
        self.mode = "w"
        self.stream = self._open()


class LoggerConfig:
    """
    Encapsulates the configuration of the root logger.
    It reads configuration settings from a YAML file via ConfigReader,
    sets up console and file handlers (using a custom ZippedRotatingFileHandler),
    and returns the configured logger.
    """

    def __init__(self, env=None):
        """
        Initialize the LoggerConfigurator with the given environment.

        Args:
            env (str): The environment identifier (e.g. "dev", "prod").
        """
        self.env = env
        self.config = ConfigReader(env="desktop", base_dir="config", module="application")

    def configure(self):
        """
        Configure and return the root logger based on the configuration settings.

        Returns:
            logging.Logger: The configured root logger.
        """
        # Retrieve logging settings from configuration.
        log_file = self.config.get("logging.log_file", "app.log")
        log_level_str = self.config.get("logging.level", "DEBUG")
        max_bytes = self.config.get("logging.max_bytes", 10000)  # 10 KB
        backup_count = self.config.get("logging.backup_count", 5)  # 5 backups
        level = getattr(logging, log_level_str.upper(), logging.DEBUG)
        log_format = self.config.get("logging.log_format",
                                     "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Ensure the log file's directory exists.
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create and configure the root logger.
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(log_format)

        # Console handler: outputs to the terminal.
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler: writes logs to a file with rotation and compression.
        file_handler = ZippedRotatingFileHandler(log_file,
                                                 maxBytes=max_bytes,
                                                 backupCount=backup_count
                                                 )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger
