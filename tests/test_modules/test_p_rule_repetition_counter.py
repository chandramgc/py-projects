import os
import unittest
import tempfile
import shutil
import xml.etree.ElementTree as ET
from collections import defaultdict
from src.modules.p_rule_repetition_counter import PRuleByRepetitionCounter


class TestPRuleByRepetitionCounter(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

        # Create sample XML files
        self._create_xml("file1.xml", [("R1", "A"), ("R1", "A")])  # R1A x2
        self._create_xml("file2.xml", [("R1", "A")])  # R1A x1
        self._create_xml("file3.xml", [("R2", "B")] * 3)  # R2B x3

    def tearDown(self):
        # Remove temporary directory after test
        shutil.rmtree(self.test_dir)

    def _create_xml(self, filename, rules):
        path = os.path.join(self.test_dir, filename)
        root = ET.Element("IFML")
        file_el = ET.SubElement(root, "File")
        message = ET.SubElement(file_el, "Message")
        payment = ET.SubElement(message, "BasicPayment")

        for rule in rules:
            pr = ET.SubElement(payment, "ProcessingRule")
            ET.SubElement(pr, "Level").text = "message"
            ET.SubElement(pr, "Type").text = "PRM"
            ep = ET.SubElement(pr, "ExecutionParm")
            ET.SubElement(ep, "ParmID").text = rule[0]
            ET.SubElement(ep, "ParmValues").text = rule[1]

        tree = ET.ElementTree(root)
        tree.write(path)

    def test_counting_logic(self):
        counter = PRuleByRepetitionCounter(
            directory=self.test_dir,
            root_xpath=".//ProcessingRule/ExecutionParm",
            key_xpaths=["ParmID", "ParmValues"]
        )

        result = counter.process()

        expected = {
            ("R1", "A"): {"1": 1, "2": 1},
            ("R2", "B"): {"3": 1}
        }

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
