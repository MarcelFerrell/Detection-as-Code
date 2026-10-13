# import subprocess for running external commands and Path from pathlib for handling filesystem paths. Also import the validate_rule function from the src.validator module to validate Sigma rules before conversion.
import subprocess
from pathlib import Path

from src.validator import validate_rule

# Find the project's detections directory by getting the current file '__file__' absolute path with .resolve() and then getting the parent directory twice to reach the project root. Then, append 'detections' to the project root path to get the detections directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DETECTIONS_DIR = PROJECT_ROOT / "detections"

# Creates a function called convert_rule that takes a file path as an argument. This function first validates the Sigma rule using the validate_rule function. If validation passes, it constructs a command to convert the Sigma rule into a Lucene query using the Sigma CLI. It then runs this command using subprocess.run and returns the converted query as a string.
def convert_rule(file_path):
    """Convert a Sigma detection into a Lucene query."""

    file_path = Path(file_path)

    # Check whether the Sigma file exists.
    if not file_path.is_file():
        raise FileNotFoundError(
            f"Sigma detection not found: {file_path}"
    )

    # Validate the Sigma detection.
    if not validate_rule(file_path):
        raise ValueError("Sigma validation failed")

    # Build the Sigma CLI command.
    command = [
        "sigma",
        "convert",
        "-t", "lucene",
        "-p", "ecs_windows",
        str(file_path),
    ]

    # Run the command and capture the output. The subprocess.run function is used to execute the command, capturing both stdout and stderr. The check=True argument ensures that an exception is raised if the command returns a non-zero exit code, indicating an error during execution.
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
    )

    # Return the converted Lucene query as a string, stripping any leading or trailing whitespace from the output. This allows the caller to receive a clean query string for further processing or display.
    return result.stdout.strip()

# If the script is run directly (not imported as a module), it will execute the code in this block. It constructs the path to a specific Sigma rule file, calls the convert_rule function to convert it into a Lucene query, and prints the resulting query to the console. This allows for quick testing and demonstration of the conversion functionality.
if __name__ == "__main__":
    rule_path = (
        DETECTIONS_DIR
        / "windows"
        / "powershell_encoded_command.yml"
    )

    query = convert_rule(rule_path)

    print("\nConverted Lucene query:")
    print(query)
