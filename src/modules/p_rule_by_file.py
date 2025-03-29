import os
import xml.etree.ElementTree as ET
from collections import defaultdict


class FileWiseByFile:
    """
    Parses multiple XML files, dynamically extracts values from a configurable root XPath,
    and then uses one or more relative key XPath expressions under that root node to count unique combinations.
    The filename is automatically added as part of the final key.
    """

    def __init__(self, directory, root_xpath, key_xpaths):
        """
        Args:
            directory (str): Directory containing XML files.
            root_xpath (str): XPath to locate the parent node (e.g., ExecutionParm) for key extraction.
            key_xpaths (list[str]): List of relative XPath expressions under the root node to extract key parts.
        """
        self.directory = directory
        self.root_xpath = root_xpath
        self.key_xpaths = key_xpaths

    def process(self):
        """
        Process all XML files and collect counts for key combinations.

        Returns:
            dict: { (key1, key2, ..., filename): count }
        """
        all_counts = defaultdict(int)
        xml_files = [f for f in os.listdir(self.directory) if f.lower().endswith(".xml")]

        for filename in sorted(xml_files):
            file_path = os.path.join(self.directory, filename)
            file_counts = self._process_file(file_path, filename)
            for key, count in file_counts.items():
                all_counts[key] += count

        return all_counts

    def _process_file(self, file_path, filename):
        """
        Processes a single XML file to extract and count key tuples from root_xpath + key_xpaths.

        Returns:
            dict: { (key1, key2, ..., filename): count }
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
                    key_tuple = tuple(keys + [filename])
                    local_counts[key_tuple] += 1

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

        return local_counts

    def print_result(self, counts):
        """
        Nicely print out the results.

        Args:
            counts (dict): Count data.
        """
        for key_tuple, count in sorted(counts.items()):
            key_str = ", ".join(key_tuple)
            print(f"({key_str}): {count}")
