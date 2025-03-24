import os
import json
import tempfile
import unittest
from src.services.report_writer import ReportWriter  # Adjust the import as needed


class TestReportWriter(unittest.TestCase):
    def test_write_counts_to_json(self):
        # Sample counts dictionary: one key is a tuple, another is a simple string.
        sample_counts = {
            ("RULE1", "VALUE1"): 2,
            "RULE2": 1
        }

        # Create a temporary directory to serve as the output directory.
        with tempfile.TemporaryDirectory() as temp_dir:
            # Instantiate ReportWriter with the temporary directory.
            writer = ReportWriter(output_dir=temp_dir)
            filename = "report_test.json"
            writer.write_counts_to_json(sample_counts, filename=filename)

            # Verify that the file was created.
            output_file = os.path.join(temp_dir, filename)
            self.assertTrue(os.path.exists(output_file))

            # Read and load the JSON file.
            with open(output_file, "r") as f:
                data = json.load(f)

            # Convert the JSON list back to a dictionary for easy comparison.
            # Tuple keys are saved as arrays (lists) in JSON, so we convert them back to tuples.
            result = {}
            for item in data:
                key = item["key"]
                # If the key is a list, convert it to a tuple.
                if isinstance(key, list):
                    key = tuple(key)
                result[key] = item["count"]

            expected = {("RULE1", "VALUE1"): 2, "RULE2": 1}
            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
