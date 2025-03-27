import logging
import os
import json
from src.utils.logger import LoggerConfig

# Retrieve a logger for this module.
logger = logging.getLogger(__name__)


class ReportWriter:
    """
        ReportWriter converts a counts dictionary (with dynamic tuple keys) into
        a nested JSON report. The grouping is performed recursively: the first
        element of the tuple becomes the outer key, and the remainder of the
        tuple is further grouped under "subValue".

        The output format is similar to:

        [
            {
                "key": "WFI$CHARGE_PARTY",
                "subValue": [
                    { "key": "B", "count": "2" },
                    { "key": "W", "count": "2" }
                ],
                "count": "4"
            },
            {
                "key": "WFI$DISCOUNT",
                "subValue": [
                    { "key": "A", "count": "4" }
                ],
                "count": "4"
            }
            // etc.
        ]
        """

    def __init__(self, output_dir="data/report"):
        """
        Initialize ReportWriter.

        Args:
            output_dir (str): Directory where the JSON report will be saved.
                              Defaults to "data/report".
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def group_dynamic(self, counts):
        """
        Recursively groups a dictionary with keys as dynamic-length tuples.

        Args:
            counts (dict): Dictionary with keys as tuples (of any length) and integer counts.

        Returns:
            list: A list of dictionaries representing the grouped structure.
        """
        groups = {}
        # Group by the first element of the tuple.
        for key, count in counts.items():
            if not key:
                continue
            outer = key[0]
            rest = key[1:]  # may be empty if key length is 1
            if outer not in groups:
                groups[outer] = {}
            groups[outer][rest] = groups[outer].get(rest, 0) + count

        result = []
        for outer, sub_counts in groups.items():
            total = sum(sub_counts.values())
            group_dict = {"key": outer, "count": str(total)}
            # If there is any remaining part (non-empty rest), recursively group them.
            if any(rest for rest in sub_counts.keys()):
                group_dict["subValue"] = self.group_dynamic(sub_counts)
            result.append(group_dict)
        result.sort(key=lambda x: x["key"])
        return result

    def write_grouped_report(self, counts, filename="report_grouped.json"):
        """
        Converts the counts dictionary into a grouped JSON structure and writes it to a file.

        Args:
            counts (dict): Dictionary with dynamic tuple keys and integer counts.
            filename (str): The filename for the JSON report.
        """
        report_data = self.group_dynamic(counts)
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(report_data, f, indent=4)
        logger.info(f"Grouped report written to {filepath}")
