# logger_config.py
import logging.config
import yaml
from dagster import get_dagster_logger as dagster_get_logger

# Global variable for the logging configuration file.
LOGGING_CONFIG_FILE = "misc/logging_config.yml"


class LoggerConfigurator:

    @staticmethod
    def apply_config(config_file=LOGGING_CONFIG_FILE):
        """
        Load the logging configuration from the given YAML file and apply it.
        """
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)

    @staticmethod
    def get_custom_logger(config_file=LOGGING_CONFIG_FILE):
        """
        Set up logging using the given configuration file and return the root logger
        or a custom logger if preferred.

        Returns:
            Logger: The configured custom logger.
        """
        LoggerConfigurator.apply_config(config_file)
        # Return the root logger or a specific custom logger if configured.
        return logging.getLogger()

    @staticmethod
    def get_dagster_logger(config_file=LOGGING_CONFIG_FILE):
        """
        Set up logging using the given configuration file and return the Dagster logger.

        Returns:
            Logger: The configured Dagster logger.
        """
        LoggerConfigurator.apply_config(config_file)
        return dagster_get_logger()
