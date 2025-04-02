import unittest
import tempfile
import shutil
import os
import json
from src.services.report_writer import ReportWriter


# Assuming ReportWriter is already defined in the current context or imported from your module
class TestReportWriterFull(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.writer = ReportWriter(output_dir=self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_write_grouped_by_repetition_counter(self):
        counts_dict = {
            ("WFI$CHARGE_PARTY", "B"): {"1": 1, "3": 1},
            ("WFI$CHARGE_PARTY", "W"): {"1": 2}
        }

        expected_output = [
            {
                "key": "WFI$CHARGE_PARTY",
                "subValue": [
                    {
                        "key": "B",
                        "counts": {"1": 1, "3": 1}
                    },
                    {
                        "key": "W",
                        "counts": {"1": 2}
                    }
                ],
                "counts": {"1": 3, "3": 1}
            }
        ]

        output_file = "nested_counts.json"
        self.writer.write_grouped_by_repetition_counter(counts_dict, output_file)

        with open(os.path.join(self.temp_dir, output_file), "r") as f:
            actual = json.load(f)

        self.assertEqual(actual, expected_output)


if __name__ == "__main__":
    unittest.main()
