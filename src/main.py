"""
Module: main
This is the entry point of the application. It loads the environment configuration,
initializes the Application, and starts the Flask API server.
"""
from typing import Any

import sys
import os
from src.utils.config_reader import ConfigReader
from src.utils.logger import LoggerConfig
from src.modules.p_rule_counter import ProcessingRuleCounter
from src.services.report_writer import ReportWriter


# Add the project root (the parent directory of src) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def main():
    """
    Main function to load configuration and start the server.
    """
    # Get the environment from the command line, default to "dev" if not provided.
    env = sys.argv[1] if len(sys.argv) > 1 else "desktop"
    logger: Any = LoggerConfig().configure()
    logger.info("Starting the application")

    # Load configuration from YAML for the 'dev' environment.
    config: Any = ConfigReader(env=env)
    profile = config.get("profile")
    logger.info(f"This application is running on {profile}")

    xml_directory = config.get("file.dir")
    xpath_expr = config.get("file.xpath_expr")
    report_directory = config.get("file.report")
    counter = ProcessingRuleCounter(xml_directory, xpath_expr=xpath_expr)
    writer = ReportWriter(report_directory)

    # Count unique keys based solely on ParmID.
    counts_by_id = counter.count_rules(key_mode="id")
    print("Processing rule counts (unique by ParmID):")
    for key, count in sorted(counts_by_id.items(), key=lambda x: x[0]):
        print(f"{key}: {count}")
    writer.write_counts_to_json(counts_by_id, "counts_by_id_report.json")

    # Count unique keys based on the combination (ParmID, ParmValues).
    counts_combined = counter.count_rules(key_mode="combined")
    print("\nProcessing rule counts (unique by (ParmID, ParmValues)):")
    for key, count in sorted(counts_combined.items(), key=lambda x: x[0]):
        print(f"{key}: {count}")
    writer.write_counts_to_json(counts_combined, "counts_combined.json")

    logger.info("Application finished execution")


if __name__ == "__main__":
    main()
