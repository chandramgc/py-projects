import os
import json
import tempfile
import unittest
from src.services.report_writer import ReportWriter  # Adjust the import as needed


class TestReportWriter(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for report output.
        self.temp_dir = tempfile.TemporaryDirectory()
        self.report_writer = ReportWriter(output_dir=self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_write_grouped_report(self):
        # Sample counts dictionary with dynamic tuple keys.
        sample_counts = {
            ("WFI$CHARGE_PARTY", "B"): 2,
            ("WFI$CHARGE_PARTY", "W"): 2,
            ("WFI$DISCOUNT", "A"): 4,
            ("WFI$COMMISSION", "D"): 1,
            ("WFI$COMMISSION", "M"): 1
        }
        expected_report = [
            {
                "key": "WFI$CHARGE_PARTY",
                "subValue": [
                    {"key": "B", "count": "2"},
                    {"key": "W", "count": "2"}
                ],
                "count": "4"
            },
            {
                "key": "WFI$COMMISSION",
                "subValue": [
                    {"key": "D", "count": "1"},
                    {"key": "M", "count": "1"}
                ],
                "count": "2"
            },
            {
                "key": "WFI$DISCOUNT",
                "subValue": [
                    {"key": "A", "count": "4"}
                ],
                "count": "4"
            }
        ]

        # Write the report.
        report_filename = "test_report.json"
        self.report_writer.write_grouped_report(sample_counts, filename=report_filename)
        report_path = os.path.join(self.temp_dir.name, report_filename)

        # Verify that the file exists.
        self.assertTrue(os.path.exists(report_path))

        # Read the JSON file.
        with open(report_path, "r") as f:
            report_data = json.load(f)

        # Sort both expected and generated lists by outer "key" for comparison.
        report_data.sort(key=lambda x: x["key"])
        expected_report.sort(key=lambda x: x["key"])
        self.assertEqual(report_data, expected_report)


if __name__ == "__main__":
    unittest.main()
