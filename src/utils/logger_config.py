# logger_config.py
import logging.config
import yaml
from dagster import get_dagster_logger as dagster_get_logger

# Global variable for the logging configuration file.
LOGGING_CONFIG_FILE = "misc/logging_config.yml"


class LoggerConfigurator:

    @staticmethod
    def get_custom_logger(config_file=LOGGING_CONFIG_FILE):
        """
        Load logging configuration from a YAML file and apply it.

        Args:
            config_file (str): Path to the logging configuration YAML file.
        """
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)

    @staticmethod
    def get_dagster_logger(config_file=LOGGING_CONFIG_FILE):
        """
        Retrieve the Dagster logger using Dagster's built-in get_dagster_logger().

        Returns:
            Logger: The configured Dagster logger.
        """
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)

        return dagster_get_logger()
