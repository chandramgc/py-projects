import unittest
import tempfile
import shutil
import os
import xml.etree.ElementTree as ET
from collections import defaultdict

from src.modules.p_rule_by_file import FileWiseByFile


class TestFileWiseByFile(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_xml_file(self, filename, rules):
        """
        Helper function to create XML with given (ParmID, ParmValues) rules.
        """
        root = ET.Element("IFML")
        file_node = ET.SubElement(root, "File")
        message = ET.SubElement(file_node, "Message")
        payment = ET.SubElement(message, "BasicPayment")

        for pid, pval in rules:
            pr = ET.SubElement(payment, "ProcessingRule")
            ET.SubElement(pr, "Level").text = "message"
            ET.SubElement(pr, "Type").text = "PRM"
            exec_parm = ET.SubElement(pr, "ExecutionParm")
            if pid is not None:
                ET.SubElement(exec_parm, "ParmID").text = pid
            if pval is not None:
                ET.SubElement(exec_parm, "ParmValues").text = pval

        tree = ET.ElementTree(root)
        tree.write(os.path.join(self.test_dir, filename))

    def test_multiple_files_counting(self):
        self.create_xml_file("file1.xml", [("R1", "X"), ("R1", "X")])
        self.create_xml_file("file2.xml", [("R1", "X"), ("R2", "Y")])

        counter = FileWiseByFile(self.test_dir, ".//ProcessingRule/ExecutionParm", ["ParmID", "ParmValues"])
        result = dict(counter.process())

        expected = {
            ("R1", "X", "file1.xml"): 2,
            ("R1", "X", "file2.xml"): 1,
            ("R2", "Y", "file2.xml"): 1
        }

        self.assertEqual(result, expected)

    def test_missing_parmvalues(self):
        self.create_xml_file("file3.xml", [("R1", None), ("R1", "Z")])
        counter = FileWiseByFile(self.test_dir, ".//ProcessingRule/ExecutionParm", ["ParmID", "ParmValues"])
        result = dict(counter.process())

        expected = {
            ("R1", "Z", "file3.xml"): 1
        }

        self.assertEqual(result, expected)

    def test_empty_valid_file(self):
        root = ET.Element("IFML")
        ET.ElementTree(root).write(os.path.join(self.test_dir, "empty.xml"))

        counter = FileWiseByFile(self.test_dir, ".//ProcessingRule/ExecutionParm", ["ParmID", "ParmValues"])
        result = dict(counter.process())

        self.assertEqual(result, {})

    def test_invalid_xml_handling(self):
        # Create malformed XML file
        with open(os.path.join(self.test_dir, "broken.xml"), "w") as f:
            f.write("<IFML><File><MissingEndTag>")

        counter = FileWiseByFile(self.test_dir, ".//ProcessingRule/ExecutionParm", ["ParmID", "ParmValues"])
        result = dict(counter.process())

        self.assertEqual(result, {})  # Should skip invalid file gracefully


if __name__ == "__main__":
    unittest.main()
