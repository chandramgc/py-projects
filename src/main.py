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
from src.modules.p_rule_counter import ProcessingRuleCounter


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

    xml_directory = config.get("file.dir")
    xpath_expr = config.get("file.xpath_expr")
    # To count based solely on ParmID, use key_mode="id"
    counter_by_id = ProcessingRuleCounter(xml_directory, xpath_expr=xpath_expr, key_mode="id")
    counts_by_id = counter_by_id.count_rules()
    print("Processing rule counts (unique by ParmID):")
    for key, count in sorted(counts_by_id.items(), key=lambda x: x[0]):
        print(f"{key}: {count}")

    # To count based on the combination (ParmID, ParmValues), use key_mode="combined"
    counter_combined = ProcessingRuleCounter(xml_directory, xpath_expr=xpath_expr, key_mode="combined")
    counts_combined = counter_combined.count_rules()
    print("\nProcessing rule counts (unique by (ParmID, ParmValues)):")
    for key, count in sorted(counts_combined.items(), key=lambda x: x[0]):
        print(f"{key}: {count}")

    logger.info("Application finished execution")


if __name__ == "__main__":
    main()
