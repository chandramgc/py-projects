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
from src.modules.p_rule_repetition_counter import PRuleByRepetitionCounter


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
    config: Any = ConfigReader(env=env, base_dir="config", module="application")
    profile = config.get("profile")
    logger.info(f"This application is running on {profile}")

    xml_dir = config.get("file.dir")
    root_xpath = config.get("file.root_xpath")
    key_prams = config.get("file.key_prams")
    key_xpaths = config.get("file.key_xpaths")
    report_directory = config.get("file.report.dir")
    report_file_name = config.get("file.report.file_name")

    writer: ReportWriter = ReportWriter(report_directory)

    # counter = ProcessingRuleCounter(xml_dir, key_xpaths)
    # rule_counts = counter.count_rules()
    # print("Rule counts (combination of keys):")
    # for key, count in sorted(rule_counts.items(), key=lambda x: x[0]):
    #     print(f"{list(key)}: {count}")   #
    #
    # writer.write_grouped_report(rule_counts, report_file_name)

    counter = PRuleByRepetitionCounter(xml_dir, root_xpath, key_prams)
    result = counter.process()
    counter.print_grouped_result(result)

    writer.write_grouped_by_repetition_counter(result, report_file_name)

    logger.info("Application finished execution")

if __name__ == "__main__":
    main()
