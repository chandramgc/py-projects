import os
import xml.etree.ElementTree as ET


class ProcessingRuleCounter:
    """
    ProcessingRuleCounter extracts keys from XML files based on a list of XPath 
    expressions and counts how many files share the same combination of keys.

    For each XML file, it extracts the value for each XPath in the list 
    (using the first occurrence). The extracted values are combined into a 
    tuple that serves as the key in the resulting count dictionary.
    """

    def __init__(self, xml_directory: str, key_xpath: list[str]):
        """
        Initialize the ProcessingRuleCounter.

        Args:
            xml_directory (str): The directory containing XML files.
            key_xpath (list of str): A list of absolute XPath expressions to extract key values.
                                      For example:
                                      [".//ProcessingRule/ExecutionParm/ParmID",
                                       ".//ProcessingRule/ExecutionParm/ParmValues"]
        """
        self.xml_directory = xml_directory
        self.key_xpath = key_xpath

    def process_file(self, filepath):
        """
        Process a single XML file by extracting key values using the provided key_xpaths.
        It pairs the extracted values by index (up to the shortest list of results).

        Args:
            filepath (str): The path to the XML file.

        Returns:
            list: A list of tuples; each tuple is a combination of extracted key values.
        """
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            # For each key_xpath, retrieve all matching elements and convert them to text.
            key_lists = []
            for xpath in self.key_xpath:
                elements = root.findall(xpath)
                values = [elem.text.strip()
                          if elem is not None and elem.text else "" for elem in elements]
                key_lists.append(values)
            if not key_lists:
                return []
            # Pair values from each list by index up to the minimum length.
            min_length = min(len(lst) for lst in key_lists)
            keys_list = []
            for i in range(min_length):
                key_tuple = tuple(lst[i] for lst in key_lists)
                keys_list.append(key_tuple)
            return keys_list
        except Exception as e:
            print(f"Error processing file {filepath}: {e}")
            return []

    def count_rules(self):
        """
        Iterate over all XML files in the directory and count the occurrence of each
        combination of key values. Every occurrence is counted
        (even if a file contains multiple occurrences).

        Returns:
            dict: A dictionary where keys are tuples (combination of extracted key values)
                  and values are the total count across all files.
        """
        counts = {}
        for filename in os.listdir(self.xml_directory):
            if filename.lower().endswith(".xml"):
                filepath = os.path.join(self.xml_directory, filename)
                keys = self.process_file(filepath)
                for key in keys:
                    counts[key] = counts.get(key, 0) + 1
        return counts

    def get_common_rules(self, file_rules=None):
        """
        Computes and returns the set of rules common to all files.

        Args:
            file_rules (dict, optional): A dictionary mapping file names to sets of rules.

        Returns:
            set: The intersection of rule sets from all files.
        """
        file_rules = file_rules if file_rules is not None else file_rules
        all_rules = list(file_rules.values())
        if not all_rules:
            return set()
        common = all_rules[0].copy()
        for rules in all_rules[1:]:
            common = common.intersection(rules)
        return common

    def get_specific_rules(self, file_rules=None):
        """
        Computes the rules that are unique (specific) to each file.

        Args:
            file_rules (dict, optional): A dictionary mapping file names to sets of rules.

        Returns:
            dict: A dictionary mapping each file name to the set of rules unique to that file.
        """
        file_rules = file_rules if file_rules is not None else file_rules
        specific = {}
        for file, rules in file_rules.items():
            others = set()
            for other_file, other_rules in file_rules.items():
                if other_file != file:
                    others = others.union(other_rules)
            specific[file] = rules - others
        return specific

    def generate_report(self, file_rules=None):
        """
        Generates a report indicating which rules are common to all files
        and which rules are specific to each file.

        Args:
            file_rules (dict, optional): A dictionary mapping file names to sets of rules.

        Returns:
            dict: A dictionary with two keys:
                  "common_rules": a list of rules common to all files,
                  "specific_rules": a dictionary mapping file names to lists of unique rules.
        """
        file_rules = file_rules if file_rules is not None else file_rules
        report = {
            "common_rules": list(self.get_common_rules(file_rules)),
            "specific_rules": {file: list(rules)
                               for file, rules in self.get_specific_rules(file_rules).items()}
        }
        return report
