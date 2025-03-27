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
    ConfigReader loads and merges multiple YAML configuration files from a given directory.
    It supports specifying an environment (e.g., "dev" or "prod") and an optional module name.
    If a module name is provided, only files whose filenames start with that module name are loaded.
    The merged configuration is available via the get() method using dot‐notation.

    Example directory structure:

        config/
            dev/
                module1-settings.yml
                module1-database.yml
                global.yml
    """

    def __init__(self, env="dev", base_dir="config", module=None):
        """
        Initialize the MultiConfigReader.

        Args:
            env (str): The environment folder to load configuration from (e.g., "dev", "prod").
                       Defaults to "dev".
            base_dir (str): The base directory where configuration folders are located.
                            Defaults to "config".
            module (str, optional): The module name to filter configuration files.
                                    Only files whose filenames start with this string will be
                                    loaded. If None, all files in the environment folder are loaded.
        """
        self.config_dir = os.path.join(base_dir, env)
        self.module = module
        self.config = self._load_all_configs()

    @staticmethod
    def deep_merge(dict1, dict2):
        """
        Recursively merge dict2 into dict1.
        If a key exists in both dictionaries and both values are dicts,
        merge them recursively. Otherwise, overwrite with dict2's value.

        Args:
            dict1 (dict): The original dictionary.
            dict2 (dict): The dictionary to merge into dict1.

        Returns:
            dict: The merged dictionary.
        """
        for key, value in dict2.items():
            if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
                ConfigReader.deep_merge(dict1[key], value)
            else:
                dict1[key] = value
        return dict1

    def _load_all_configs(self):
        """
        Loads and deep-merges all YAML files in the configuration directory.
        If a module name is provided, only those files whose filenames start with the
        module name are loaded.

        Returns:
            dict: The merged configuration dictionary.
        """
        merged_config = {}
        for filename in os.listdir(self.config_dir):
            if filename.lower().endswith((".yml", ".yaml")):
                # If module is provided, skip files that don't start with the module name.
                if self.module and not filename.startswith(self.module):
                    continue
                file_path = os.path.join(self.config_dir, filename)
                with open(file_path, "r") as f:
                    config_data = yaml.safe_load(f) or {}
                    merged_config = self.deep_merge(merged_config, config_data)
        return merged_config

    def get(self, key, default=None):
        """
        Retrieve a nested configuration value using a dot-separated key.

        Args:
            key (str): Dot-separated key string (e.g., "server.port").
            default: Value to return if the key is not found.

        Returns:
            The configuration value or default if not found.
        """
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, None)
            else:
                return default
            if value is None:
                return default
        return value
