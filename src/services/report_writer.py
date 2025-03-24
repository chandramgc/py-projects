import logging
import os
import json
from src.utils.logger import LoggerConfig

# Retrieve a logger for this module.
logger = logging.getLogger(__name__)


class ReportWriter:
    """
    A class to write count reports to JSON files.
    It converts tuple keys to arrays so that the output is JSON compatible.
    """

    def __init__(self, output_dir="data/report"):
        """
        Initialize the ReportWriter.

        Args:
            output_dir (str, optional): The directory where the JSON report will be saved.
                                        Defaults to "data/report".
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def write_counts_to_json(self, counts, filename="report.json"):
        """
        Write the counts dictionary to a JSON file.
        If a key is a tuple, it is converted to a list (JSON array).

        Args:
            counts (dict): The counts dictionary (keys are either strings or tuples).
            filename (str, optional): The filename to write the report to.
            Defaults to "report.json".
        """
        output_list = []
        for key, count in counts.items():
            json_key = list(key) if isinstance(key, tuple) else key
            output_list.append({"key": json_key, "count": count})
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(output_list, f, indent=4)
        logger.info(f"Report written to {filepath}")
