import os
import unittest
from src.modules.p_rule_counter import ProcessingRuleCounter  # Adjust import if necessary


class TestProcessingRuleCounter(unittest.TestCase):
    def setUp(self):
        self.base = "data"
        self.test_folder = os.path.join(self.base, "test_files")

    def test_count_rules(self):
        # Use absolute XPath expressions for keys.
        key_xpaths = [
            ".//ProcessingRule/ExecutionParm/ParmID",
            ".//ProcessingRule/ExecutionParm/ParmValues"
        ]
        # Instantiate DynamicRuleCounter with the temporary XML directory.
        counter = ProcessingRuleCounter(self.test_folder, key_xpaths)
        counts = counter.count_rules()

        # Expected:
        # From file1.xml:
        #   ("WFI$CHARGE_PARTY", "B") appears once,
        #   ("WFI$DISCOUNT", "A") appears once.
        # From file2.xml:
        #   ("WFI$CHARGE_PARTY", "W") appears once,
        #   ("WFI$DISCOUNT", "A") appears once.
        expected_counts = {
            ("WFI$CHARGE_PARTY", "B"): 1,
            ("WFI$DISCOUNT", "A"): 2,  # appears in both files
            ("WFI$CHARGE_PARTY", "W"): 1
        }
        self.assertEqual(counts, expected_counts)


if __name__ == "__main__":
    unittest.main()
