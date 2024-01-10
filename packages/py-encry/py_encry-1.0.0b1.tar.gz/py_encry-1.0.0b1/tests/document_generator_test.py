from src.pyencry.document_generator import DocumentGenerator
import unittest
import json

class DocumentGeneratorTests(unittest.TestCase):
    def test_can_create_document(self):
        docstrings = DocumentGenerator("./data/document_generator_test.py")
        info = docstrings.parse_docstring()
        json_info = json.dumps(info)
        with open("./data/expected_docoment_generator.json", "r") as file:
            expected = file.read()
        self.assertEqual(json_info, expected)