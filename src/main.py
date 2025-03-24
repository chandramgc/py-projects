"""
Module: main
This is the entry point of the application. It loads the environment configuration,
initializes the Application, and starts the Flask API server.
"""
from typing import Any

import sys
import os
from src.utils.config_reader import ConfigReader
from src.utils.logger import setup_logger


# Add the project root (the parent directory of src) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def main():
    """
    Main function to load configuration and start the server.
    """
    # Get the environment from the command line, default to "dev" if not provided.
    env = sys.argv[1] if len(sys.argv) > 1 else "desktop"
    logger: Any = setup_logger()
    logger.info("Starting the application")

    # Load configuration from YAML for the 'dev' environment.
    config: Any = ConfigReader(env=env)
    profile = config.get("profile")
    logger.info(f"This application is running on {profile}")
    logger.info("Application finished execution")


if __name__ == "__main__":
    main()
