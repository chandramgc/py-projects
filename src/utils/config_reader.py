"""
Module: config_reader
This module provides the ConfigReader class to read application environment settings
from YAML configuration files.
"""
import logging
import os
import yaml

# Retrieve a logger for this module.
logger = logging.getLogger(__name__)


class ConfigReader:
    """
    Loads application settings from YAML configuration files.

    Attributes:
        config_file (str): The path to the configuration YAML file.
        config (dict): The loaded configuration data.
    """

    def __init__(self, env="dev"):
        """
        Initializes the ConfigReader for the specified environment.

        Args:
            env (str, optional): The environment identifier (e.g., "dev", "prod").
                                 Defaults to "dev".
        """
        self.config_file = f"config/application-{env}.yml"
        self.config = self._load_config()

    def _load_config(self):
        """
        Loads the YAML configuration file.

        Returns:
            dict: The configuration data.

        Raises:
            FileNotFoundError: If the configuration file is not found.
        """
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file {self.config_file} not found!")

        with open(self.config_file, "r") as file:
            return yaml.safe_load(file)

    def get(self, key, default=None):
        """
        Retrieves a nested configuration value based on a dot-separated key.

        Args:
            key (str): Dot-separated key string (e.g., "server.port").
            default (any, optional): Default value if the key is not found. Defaults to None.

        Returns:
            any: The configuration value or the default if not found.
        """
        keys = key.split(".")
        value = self.config
        for k in keys:
            value = value.get(k, {})
        return value or default
