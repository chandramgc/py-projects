import logging
import os
import json
from collections import defaultdict

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

    def write_grouped_by_keys_filename(self, counts: dict, filename: str):
        """
            Groups the counts dictionary by key tuple (excluding filename), and
            nests filenames underneath.

            Example structure:
            {
                (ParmID, ParmValues): {
                    filename: count
                }
            }

            Args:
                counts (dict): Flat counts dictionary with full key (ParmID, ParmValues, filename)
                output_file (str): Path to output JSON file
            """
        grouped = defaultdict(dict)

        for key_tuple, count in counts.items():
            *rule_keys, filename = key_tuple
            grouped[tuple(rule_keys)][filename] = count

        # Convert tuple keys to strings for JSON serialization
        grouped_serializable = {
            str(k): v for k, v in grouped.items()
        }
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(grouped_serializable, f, indent=4)

        logger.info(f"JSON written to: {filepath}")

    def nest_keys_recursively(self, counts_dict):
        """
        Recursively builds a nested dict structure from multi-part tuple keys.
        Adds 'counts' at each group level by summing nested counts.

        Example Input:
            { ("A", "B"): { "1": 2, "3": 1 }, ("A", "C"): { "1": 4 } }

        Output:
        [
            {
                "key": "A",
                "subValue": [
                    {
                        "key": "B",
                        "counts": { "1": 2, "3": 1 }
                    },
                    {
                        "key": "C",
                        "counts": { "1": 4 }
                    }
                ],
                "counts": {
                    "1": 6,
                    "3": 1
                }
            }
        ]
        """

        def merge_counts(c1, c2):
            result = defaultdict(int, c1)
            for k, v in c2.items():
                result[k] += v
            return result

        def insert_nested(current_level, key_parts, count_dict):
            key = key_parts[0]
            rest = key_parts[1:]

            for entry in current_level:
                if entry["key"] == key:
                    break
            else:
                entry = {"key": key}
                current_level.append(entry)

            if rest:
                if "subValue" not in entry:
                    entry["subValue"] = []
                insert_nested(entry["subValue"], rest, count_dict)

                # Recalculate group-level counts
                group_counts = defaultdict(int)
                for sub in entry["subValue"]:
                    for k, v in sub.get("counts", {}).items():
                        group_counts[k] += v
                entry["counts"] = dict(group_counts)
            else:
                entry["counts"] = dict(count_dict)

        result = []
        for key_tuple, count_dict in counts_dict.items():
            insert_nested(result, list(key_tuple), count_dict)

        return result

    def write_grouped_by_repetition_counter(self, counts_dict, filename):
        """
        Build nested structure dynamically from key tuples and write to JSON.
        """
        nested_data = self.nest_keys_recursively(counts_dict)

        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(nested_data, f, indent=4)

        logger.info(f"JSON written to: {filepath}")
