
# Import necessary modules globally. The 'pathlib' module is used for filesystem path manipulations, and the 'sigma' package provides classes and functions for working with Sigma rules and their validation.
from pathlib import Path
from sigma.rule import SigmaRule
from sigma.validation import SigmaValidator
from sigma.validators.core.condition import DanglingConditionValidator


# Find the project's detections directory by getting the current file '__file__' absolute path with .resolve() and then getting the parent directory twice to reach the project root. Then, append 'detections' to the project root path to get the detections directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DETECTIONS_DIR = PROJECT_ROOT / "detections" # / appends detections to the project root path

# Creates a function called validate_rule that takes a file path as an argument. This function reads the content of the file, parses it as a Sigma rule, and prints whether the validation passed or failed. It returns True if the validation passed and False if it failed.
def validate_rule(file_path):
    """Validate one Sigma detection file."""

    try:
        # Read the YAML file.
        rule_text = file_path.read_text(encoding="utf-8")

        # Parse and validate the Sigma rule.
        rule = SigmaRule.from_yaml(rule_text)

        # Check that condition references point to existing selections.
        for condition in rule.detection.parsed_condition:
            condition.parse(True)

        # Create a validator with a condition reference check.
        validator = SigmaValidator(
            validators=[DanglingConditionValidator]
        )

        # Run the validation checks.
        issues = validator.validate_rule(rule)

        # Print the validation result for the file. If there are any issues, print a warning message for each issue. If there are no issues, print a pass message with the rule title.
        if issues:
            for issue in issues:
                print(f"WARNING: {file_path.name} - {issue}")

            return False
                
        else:
            print(f"PASS: {file_path.name} - {rule.title}")
            return True

    except Exception as error:
        print(f"FAIL: {file_path.name} - {error}")
        return False

# Creates a function called validate_all that validates every Sigma detection file in the repository. It searches for all .yml and .yaml files in the detections directory, validates each file using the validate_rule function, and prints a summary of the results. It returns True if all validations passed and False if any failed.
def validate_all():
    """Validate every Sigma detection in the repository."""

    # Search for all .yml and .yaml files recursively in the detections directory and sort them.
    files = sorted(
        list(DETECTIONS_DIR.rglob("*.yml"))
        + list(DETECTIONS_DIR.rglob("*.yaml"))
    )

    if not files:
        print("ERROR: No Sigma detection files found.")
        return False
    # Initialize an empty list to store the validation results for each file.
    results = []
    # Loop through each file path in the list of files, validate it using the validate_rule function, and append the result (True or False) to the results list.
    for file_path in files:
        result = validate_rule(file_path)
        results.append(result)

    print()
    print(f"Total rules: {len(results)}") # len(results) gives the total number of validation results, which corresponds to the total number of Sigma detection files processed.
    print(f"Passed: {sum(results)}") # sum(results) counts the number of True values in the results list, which represents the number of passed validations.
    print(f"Failed: {len(results) - sum(results)}") # len(results) - sum(results) calculates the number of failed validations by subtracting the number of passed validations from the total number of rules.

    return all(results)

# The following code block checks if the script is being run directly (not imported as a module). If it is, it calls the validate_all function to validate all Sigma detection files. If any validation fails (i.e., validate_all returns False), it raises a SystemExit exception with a status code of 1, indicating an error occurred.
if __name__ == "__main__":
    if not validate_all():
        raise SystemExit(1)
