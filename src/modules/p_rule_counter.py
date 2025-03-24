import os
import xml.etree.ElementTree as ET


class ProcessingRuleCounter:
    """
    A class to count processing rule occurrences in XML files dynamically.
    The uniqueness key can be either just the rule identifier (ParmID) or
    the combination of the rule identifier and the rule value (ParmID, ParmValues).
    """

    def __init__(self, directory, xpath_expr, id_tag="ParmID", values_tag="ParmValues", key_mode="combined"):
        """
        Initialize the ProcessingRuleCounter.

        Args:
            directory (str): The path to the directory containing XML files.
            xpath_expr (str, optional): The XPath expression to locate the parent element that contains rule data.
                                        Defaults to ".//ProcessingRule/ExecutionParm".
            id_tag (str, optional): The XML tag used for the rule identifier. Defaults to "ParmID".
            values_tag (str, optional): The XML tag used for the rule values. Defaults to "ParmValues".
            key_mode (str, optional): Determines the key for uniqueness.
                                      "id" for using only ParmID, or "combined" for using (ParmID, ParmValues).
                                      Defaults to "combined".
        """
        self.directory = directory
        self.xpath_expr = xpath_expr
        self.id_tag = id_tag
        self.values_tag = values_tag
        self.key_mode = key_mode  # "id" or "combined"
        self.rule_counts = {}  # Keys are determined by key_mode

    def process_file(self, filepath):
        """
        Process a single XML file to extract unique rule keys based on the dynamic configuration.

        Args:
            filepath (str): The file path of the XML file.

        Returns:
            set: A set of unique keys (either ParmID or (ParmID, ParmValues)) found in the file.
        """
        found_keys = set()
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            rule_elements = root.findall(self.xpath_expr)
            for elem in rule_elements:
                id_elem = elem.find(self.id_tag)
                if id_elem is None or not id_elem.text:
                    continue
                rule_id = id_elem.text.strip()

                # Determine key based on key_mode
                if self.key_mode == "combined":
                    values_elem = elem.find(self.values_tag)
                    rule_value = ""
                    if values_elem is not None and values_elem.text:
                        rule_value = values_elem.text.strip()
                    # Only add if both rule_id and rule_value are present
                    if rule_id and rule_value:
                        key = (rule_id, rule_value)
                        found_keys.add(key)
                elif self.key_mode == "id":
                    # Use only the rule_id as the key
                    if rule_id:
                        found_keys.add(rule_id)
                else:
                    # Fallback: use combined
                    values_elem = elem.find(self.values_tag)
                    rule_value = ""
                    if values_elem is not None and values_elem.text:
                        rule_value = values_elem.text.strip()
                    if rule_id and rule_value:
                        key = (rule_id, rule_value)
                        found_keys.add(key)
        except Exception as e:
            print(f"Error processing file {filepath}: {e}")
        return found_keys

    def count_rules(self):
        """
        Iterate over all XML files in the directory and count the occurrences of each unique key.
        Each key (determined by key_mode) is counted only once per file.

        Returns:
            dict: A dictionary with keys (either ParmID or (ParmID, ParmValues)) and values as the count of files.
        """
        for filename in os.listdir(self.directory):
            if filename.lower().endswith(".xml"):
                filepath = os.path.join(self.directory, filename)
                file_keys = self.process_file(filepath)
                for key in file_keys:
                    self.rule_counts[key] = self.rule_counts.get(key, 0) + 1
        return self.rule_counts
