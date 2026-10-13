# Detection-as-Code Pipeline

A Python-based Detection-as-Code (DaC) pipeline for managing, validating, testing, and converting Sigma detection rules through automated CI workflows.

The project uses Sigma as a vendor-neutral detection format. It currently supports Sigma-to-Lucene conversion for Elastic and uses GitHub Actions for automated quality checks.

## Features

- **Sigma Rule Management:** Store detection rules as YAML files in a Git repository.
- **Sigma Validation:** Validate rule syntax, structure, and detection condition references with pySigma.
- **Sigma Conversion:** Convert Sigma rules into Lucene queries using Sigma CLI and the Elasticsearch backend.
- **Automated Unit Testing:** Use Python's built-in `unittest` framework to test validation and conversion.
- **Continuous Integration:** Run validation and unit tests automatically through GitHub Actions.
- **Error Handling:** Report invalid rules, missing files, and conversion failures.

## Project Structure

```text
Detection-as-Code/
├── .github/
│   └── workflows/
│       └── validate.yml
├── detections/
│   └── windows/
│       └── powershell_encoded_command.yml
├── src/
│   ├── __init__.py
│   ├── validator.py
│   └── converter.py
├── tests/
│   ├── test_validator.py
│   └── test_converter.py
├── .gitignore
└── README.md
```

## Technologies

- Python
- Sigma
- pySigma
- Sigma CLI
- Elasticsearch Sigma Backend
- Git and GitHub
- GitHub Actions
- Python unittest

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/MarcelFerrell/Detection-as-Code.git
cd Detection-as-Code
```

### 2. Create a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install sigma-cli pysigma
sigma plugin install elasticsearch
```

### 4. Verify Sigma installation

```bash
sigma list targets
sigma list pipelines
```

Confirm that the `lucene` target and `ecs_windows` processing pipeline are available.

## Usage

### Validate all Sigma detections

```bash
python -m src.validator
```

The validator searches the `detections/` directory for `.yml` and `.yaml` files.

It attempts to parse each rule and checks detection condition references.

Example output:

```text
PASS: powershell_encoded_command.yml - PowerShell Encoded Command

Total rules: 1
Passed: 1
Failed: 0
```

The command returns a nonzero exit status if validation fails.

### Convert a Sigma rule to Lucene

Using Sigma CLI:

```bash
sigma convert -t lucene -p ecs_windows detections/windows/powershell_encoded_command.yml
```

Or using the Python converter:

```bash
python -m src.converter
```

The Python converter first validates the rule and then executes Sigma CLI.

The generated Lucene query is printed to the terminal.

### Run automated tests

```bash
python -m unittest discover -s tests -v
```

The current test suite contains five tests:

1. Valid Sigma rule validation
2. Invalid YAML rejection
3. Undefined detection selection rejection
4. Successful Sigma-to-Lucene conversion
5. Missing detection file handling

## Continuous Integration

The project uses GitHub Actions.

The workflow is defined in:

`.github/workflows/validate.yml`

The workflow runs automatically when code is pushed or a pull request is opened or updated.

It performs the following operations:

1. Downloads the repository.
2. Configures Python 3.12.
3. Installs Sigma and its Elasticsearch plugin.
4. Validates all Sigma detection files.
5. Executes the Python unit tests.

If validation or testing fails, GitHub Actions marks the workflow as failed.

The current CI workflow does not convert every detection in the repository. Conversion is covered by the existing unit test for the example rule.

## Current Limitations

- No SIEM connection or automated deployment.
- Lucene conversion is configured for Windows detections using the ECS processing pipeline.
- No automated testing against real security events.
- No repository-wide conversion checks.
- No automated rollback or deployment verification.
- Successful validation does not guarantee that a detection is accurate or effective.

## Development Roadmap

- [x] Create a Sigma detection repository
- [x] Implement Sigma validation in Python
- [x] Add validation unit tests
- [x] Implement Sigma-to-Lucene conversion
- [x] Add converter unit tests
- [x] Configure GitHub Actions CI
- [ ] Add repository-wide conversion tests
- [ ] Implement detection logic tests using sample events
- [ ] Add Sigma-to-SPL conversion
- [ ] Implement automated rule quality checks
- [ ] Add controlled SIEM deployment
- [ ] Implement deployment verification and rollback
- [ ] Support multiple SIEM environments

## Project Status

**Status:** Early development — CI pipeline operational.

The current system provides a foundation for validating and converting Sigma detections without requiring a running SIEM.

The long-term goal is to support a complete detection lifecycle, from rule development and automated testing to controlled deployment and maintenance.