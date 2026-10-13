# Imports unittest for creating test cases, tempfile for creating temporary files and directories, and Path from pathlib for handling filesystem paths. It also imports the validate_rule function from the src.validator module to be tested.
import unittest
import tempfile
from pathlib import Path

from src.validator import validate_rule

# Defines a test case class TestSigmaValidator that inherits from unittest.TestCase. This class contains methods to test the validate_rule function with different scenarios.
class TestSigmaValidator(unittest.TestCase):

    # Defines a test method test_valid_rule that checks if a valid Sigma rule passes validation. It constructs the path to a known valid Sigma rule file, calls validate_rule with that path, and asserts that the result is True (indicating the rule passed validation).
    def test_valid_rule(self):
        """A valid Sigma rule should pass."""

        # Constructs the path to a known valid Sigma rule file located in the detections/windows directory. It uses Path to create a path object pointing to the powershell_encoded_command.yml file.
        rule_path = Path(
            "detections/windows/powershell_encoded_command.yml"
        )

        # Calls the validate_rule function with the constructed rule_path and stores the result (True or False) in the variable result.
        result = validate_rule(rule_path)

        # Asserts that the result is True, meaning the valid Sigma rule passed validation. If the assertion fails, the test will report an error.
        self.assertTrue(result)

    # Defines a test method test_invalid_yaml that checks if an invalid YAML file fails validation. It creates a temporary directory and writes an invalid YAML string to a file named invalid.yml. It then calls validate_rule with the path to this file and asserts that the result is False (indicating the rule failed validation).
    def test_invalid_yaml(self):
        """Invalid YAML should fail."""

    # Uses a context manager to create a temporary directory that will be automatically cleaned up after the test. Inside this directory, it creates a file named invalid.yml and writes an invalid YAML string to it. It then calls validate_rule with the path to this file and asserts that the result is False, indicating that the invalid YAML failed validation.
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "invalid.yml"

            file_path.write_text(
                "title: [invalid",
                encoding="utf-8"
            )

            result = validate_rule(file_path)

            self.assertFalse(result)

    
    def test_unknown_selection(self):
        """A Sigma condition with an undefined selection should fail."""

        rule_path = Path(
            "detections/windows/powershell_encoded_command.yml"
        )

        rule_text = rule_path.read_text(encoding="utf-8")

        invalid_rule = rule_text.replace(
            "condition: selection",
            "condition: nonexistentselection"
        )

        self.assertNotEqual(rule_text, invalid_rule)

        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "invalid_condition.yml"

            file_path.write_text(
                invalid_rule,
                encoding="utf-8"
            )

            result = validate_rule(file_path)

            self.assertFalse(result)


# Checks if the script is being run directly (not imported as a module). If it is, it calls unittest.main() to run all the test cases defined in the TestSigmaValidator class. This allows the tests to be executed when the script is run.
if __name__ == "__main__":
    unittest.main()
