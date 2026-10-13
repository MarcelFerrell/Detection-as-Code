# import unittest for creating and running unit tests, and Path from pathlib for handling filesystem paths. Also import the convert_rule function from the src.converter module to test the Sigma rule conversion functionality.
import unittest
from pathlib import Path

from src.converter import convert_rule

# Defines a test case class TestSigmaConverter that inherits from unittest.TestCase. This class contains methods to test the convert_rule function with different scenarios, including valid conversions and handling of missing files.
class TestSigmaConverter(unittest.TestCase):

    # Defines a test method test_valid_conversion that checks if a valid Sigma rule can be successfully converted to a Lucene query. It constructs the path to a known valid Sigma rule file, calls convert_rule with that path, and asserts that the returned query is a non-empty string containing the expected field.
    def test_valid_conversion(self):
        """A valid Sigma rule should convert to Lucene."""

        rule_path = Path(
            "detections/windows/powershell_encoded_command.yml"
        )

        query = convert_rule(rule_path)

        # Asserts that the returned query is a string, has a length greater than zero, and contains the expected field "process.command_line". These assertions ensure that the conversion was successful and produced a valid Lucene query.
        self.assertIsInstance(query, str)
        self.assertTrue(len(query) > 0)
        self.assertIn("process.command_line", query)

    # Defines a test method test_missing_file that checks if the convert_rule function raises a FileNotFoundError when given a path to a nonexistent Sigma rule file. It constructs the path to a missing file and uses assertRaises to verify that the expected exception is raised.
    def test_missing_file(self):
        """A nonexistent Sigma file should fail."""

        rule_path = Path("detections/missing_rule.yml")

        # Uses assertRaises to check that calling convert_rule with the path to a nonexistent file raises a FileNotFoundError. This test ensures that the function correctly handles cases where the specified Sigma rule file does not exist.
        with self.assertRaises(FileNotFoundError):
            convert_rule(rule_path)

# If the script is run directly (not imported as a module), it will execute the code in this block. It calls unittest.main() to run all the test cases defined in the TestSigmaConverter class, allowing for automated testing of the Sigma rule conversion functionality.
if __name__ == "__main__":
    unittest.main()
