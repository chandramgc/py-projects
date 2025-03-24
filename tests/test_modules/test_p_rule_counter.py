import os
import unittest
from src.modules.p_rule_counter import ProcessingRuleCounter  # Adjust import if necessary


class TestProcessingRuleCounter(unittest.TestCase):
    def setUp(self):
        self.base = "data"
        self.test_folder = os.path.join(self.base, "test_files")
        self.xpath_expr = ".//ProcessingRule/ExecutionParm"

    def test_count_rules_id_mode(self):
        """
        For key_mode 'id', only the ParmID is used.
        Expected:
          - RULE1 appears in file1, file2, and file3 (once per file) -> count 3
          - RULE2 appears only in file1 -> count 1
          - RULE3 appears only in file2 -> count 1
        """

        counter = ProcessingRuleCounter(self.test_folder, xpath_expr=self.xpath_expr)
        counts = counter.count_rules(key_mode="id")
        expected = {
            "RULE1": 3,
            "RULE2": 1,
            "RULE3": 1,
        }
        self.assertEqual(counts, expected)

    def test_count_rules_combined_mode(self):
        """
        For key_mode 'combined', both ParmID and ParmValues are used.
        Expected:
          - ("RULE1", "VALUE1") appears in file1 and file2 -> count 2
          - ("RULE2", "VALUE2") appears only in file1 -> count 1
          - ("RULE3", "VALUE3") appears only in file2 -> count 1
          - ("RULE1", "DIFFERENT") appears in file3 -> count 1
        """
        counter = ProcessingRuleCounter(self.test_folder, xpath_expr=self.xpath_expr)
        counts = counter.count_rules(key_mode="combined")
        expected = {
            ("RULE1", "VALUE1"): 2,
            ("RULE2", "VALUE2"): 1,
            ("RULE3", "VALUE3"): 1,
            ("RULE1", "DIFFERENT"): 1,
        }
        self.assertEqual(counts, expected)


if __name__ == "__main__":
    unittest.main()
