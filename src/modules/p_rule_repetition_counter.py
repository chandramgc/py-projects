import os
import xml.etree.ElementTree as ET
from collections import defaultdict


class PRuleByRepetitionCounter:
    """
    Parses multiple XML files, dynamically extracts values from a configurable root XPath,
    and uses relative key XPath expressions to count how often each key combination occurs per file.
    Final result groups by key (e.g., (ParmID, ParmValues)) and counts how many files had that combo
    N times.
    """

    def __init__(self, directory, root_xpath, key_xpaths):
        self.directory = directory
        self.root_xpath = root_xpath
        self.key_xpaths = key_xpaths

    def process(self):
        """
        Process all XML files and return nested summary:
        {
            (key1, key2): {
                "1": 2,  # 2 files had this key once
                "2": 1   # 1 file had this key twice
            },
            ...
        }
        """
        grouped_counts = defaultdict(lambda: defaultdict(int))

        xml_files = [f for f in os.listdir(self.directory) if f.lower().endswith(".xml")]

        for filename in sorted(xml_files):
            file_path = os.path.join(self.directory, filename)
            file_counts = self._count_keys_in_file(file_path)

            for key_tuple, count in file_counts.items():
                grouped_counts[key_tuple][str(count)] += 1

        return grouped_counts

    def _count_keys_in_file(self, file_path):
        """
        Count how many times each (key1, key2, ...) tuple appears in a single file.

        Returns:
            dict: { (key1, key2): count_in_this_file }
        """
        local_counts = defaultdict(int)
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            for element in root.findall(self.root_xpath):
                keys = []
                for xpath in self.key_xpaths:
                    sub_elem = element.find(xpath)
                    value = sub_elem.text.strip() if sub_elem is not None and sub_elem.text else None
                    keys.append(value)

                if all(keys):
                    key_tuple = tuple(keys)
                    local_counts[key_tuple] += 1

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

        return local_counts

    def print_grouped_result(self, grouped_counts):
        """
        Print the grouped result in your desired format.

        Args:
            grouped_counts (dict): Output of process()
        """
        for key, file_dist in sorted(grouped_counts.items()):
            print(f"{key}: {file_dist}")
