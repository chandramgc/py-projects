import os
import xml.etree.ElementTree as ET


class ProcessingRuleCounter:
    """
    A class to count processing rule occurrences in XML files dynamically.
    The uniqueness key can be either just the rule identifier (ParmID) or
    the combination of the rule identifier and the rule value (ParmID, ParmValues).
    """

    def __init__(self, directory, xpath_expr=None, id_tag="ParmID", values_tag="ParmValues"):
        """
        Initialize the ProcessingRuleCounter.

        Args:
            directory (str): The path to the directory containing XML files.
            xpath_expr (str, optional): The XPath expression to locate the parent element that
                                        contains rule data.
                                        Defaults to ".//ProcessingRule/ExecutionParm".
            id_tag (str, optional): The XML tag used for the rule identifier. Defaults to "ParmID".
            values_tag (str, optional): The XML tag used for the rule values. Defaults to
                                        "ParmValues".
        """
        self.directory = directory
        self.xpath_expr = xpath_expr
        self.id_tag = id_tag
        self.values_tag = values_tag

    def process_file(self, filepath, key_mode="combined"):
        """
        Process a single XML file to extract unique rule keys based on the given key mode.

        Args:
            filepath (str): The file path of the XML file.
            key_mode (str, optional): Determines the key for uniqueness.
                                      "id" for using only ParmID, or "combined" for
                                      using (ParmID, ParmValues).
                                      Defaults to "combined".

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
                if key_mode == "combined":
                    values_elem = elem.find(self.values_tag)
                    rule_value = ""
                    if values_elem is not None and values_elem.text:
                        rule_value = values_elem.text.strip()
                    if rule_id and rule_value:
                        key = (rule_id, rule_value)
                        found_keys.add(key)
                elif key_mode == "id":
                    found_keys.add(rule_id)
                else:
                    # Default to combined if key_mode is unknown.
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

    def count_rules(self, key_mode="combined"):
        """
        Iterate over all XML files in the directory and count the occurrences of each unique key.
        Each key (determined by key_mode) is counted only once per file.

        Args:
            key_mode (str, optional): Determines the key for uniqueness.
                                      "id" for using only ParmID, or "combined" for
                                      using (ParmID, ParmValues).
                                      Defaults to "combined".

        Returns:
            dict: A dictionary with keys (either ParmID or (ParmID, ParmValues))
                                     and values as the count of files.
        """
        rule_counts = {}
        for filename in os.listdir(self.directory):
            if filename.lower().endswith(".xml"):
                filepath = os.path.join(self.directory, filename)
                file_keys = self.process_file(filepath, key_mode)
                for key in file_keys:
                    rule_counts[key] = rule_counts.get(key, 0) + 1
        return rule_counts
