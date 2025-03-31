import os
import logging
import logging.handlers
from src.utils.zipped_rotating_file import ZippedRotatingFileHandler
from src.utils.config_reader import ConfigReader


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
