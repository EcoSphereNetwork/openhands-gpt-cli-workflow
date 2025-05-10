#!/usr/bin/env python3
"""
Test and Report Script

This script runs tests on a repository, creates GitHub issues for failures,
and triggers OpenHands to fix the issues.
"""

import subprocess
import requests
import json
import os
import sys
import time
import argparse
from pathlib import Path

# Constants
OPENHANDS_API_URL = "http://localhost:17244/api/tasks"
GITHUB_LABEL = "fix-me"


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Run tests and report issues')
    parser.add_argument('--repo-path', type=str, default=os.getcwd(),
                        help='Path to the repository to test')
    parser.add_argument('--test-command', type=str, default='npm test',
                        help='Command to run tests')
    parser.add_argument('--skip-openhands', action='store_true',
                        help='Skip triggering OpenHands')
    return parser.parse_args()


def run_tests(repo_path, test_command):
    """Run tests in the specified repository"""
    print(f"Running tests in {repo_path} with command: {test_command}")

    # Change to the repository directory
    original_dir = os.getcwd()
    os.chdir(repo_path)

    try:
        # Run the test command
        test_result = subprocess.run(
            test_command,
            shell=True,
            capture_output=True,
            text=True
        )

        # Change back to the original directory
        os.chdir(original_dir)

        return test_result
    except Exception as e:
        print(f"Error running tests: {e}")
        # Change back to the original directory
        os.chdir(original_dir)
        return None


def create_github_issue(test_output, error_message, repo_path):
    """Create a GitHub issue with test failure details"""
    print("Creating GitHub issue...")

    # Get repository name from git config
    try:
        repo_url = subprocess.run(
            ['git', 'config', '--get', 'remote.origin.url'],
            cwd=repo_path,
            capture_output=True,
            text=True
        ).stdout.strip()

        # Extract owner/repo from URL
        repo_name = repo_url.split('/')[-2] + '/' + repo_url.split('/')[-1].replace('.git', '')
    except Exception as e:
        print(f"Error getting repository name: {e}")
        repo_name = "unknown/repository"

    # Format the issue body
    issue_body = f"""
## Test Failure
{error_message}

## Full Test Output
```
{test_output}
```

## Repository Information
- **Repository**: {repo_name}
- **Path**: {repo_path}
- **Test Command**: {args.test_command}

## Metadata
- **Label**: {GITHUB_LABEL}
- **Priority**: high
- **Run ID**: {time.strftime('%Y%m%d%H%M%S')}
"""

    # Create the issue using GitHub CLI
    result = subprocess.run(
        ['gh', 'issue', 'create',
         '--title', f'Test Failure: {error_message[:50]}...',
         '--body', issue_body,
         '--label', GITHUB_LABEL],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Error creating GitHub issue: {result.stderr}")
        return None

    # Extract issue number from the result
    issue_url = result.stdout.strip()
    issue_number = issue_url.split('/')[-1]

    print(f"Created issue #{issue_number}: {issue_url}")
    return issue_number


def trigger_openhands(issue_number, repo_path):
    """Trigger OpenHands API to fix the issue"""
    print(f"Triggering OpenHands to fix issue #{issue_number}...")

    # Get repository name from git config
    try:
        repo_url = subprocess.run(
            ['git', 'config', '--get', 'remote.origin.url'],
            cwd=repo_path,
            capture_output=True,
            text=True
        ).stdout.strip()

        # Extract owner/repo from URL
        repo_name = repo_url.split('/')[-2] + '/' + repo_url.split('/')[-1].replace('.git', '')
    except Exception as e:
        print(f"Error getting repository name: {e}")
        repo_name = "unknown/repository"

    payload = {
        'command': 'fix-test-errors',
        'context': {
            'issue_number': issue_number,
            'repository': repo_name,
            'repo_path': repo_path
        }
    }

    try:
        response = requests.post(
            OPENHANDS_API_URL,
            json=payload
        )

        if response.status_code == 200:
            print(f"Successfully triggered OpenHands: {response.json()}")
            return True
        else:
            print(f"Error triggering OpenHands: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"Exception while triggering OpenHands: {e}")
        return False


def main():
    global args
    args = parse_args()

    # Ensure the repository path exists
    repo_path = Path(args.repo_path).resolve()
    if not repo_path.exists() or not repo_path.is_dir():
        print(f"Error: Repository path {repo_path} does not exist or is not a directory")
        return 1

    # Run the tests
    test_result = run_tests(repo_path, args.test_command)
    if test_result is None:
        print("Failed to run tests. Exiting.")
        return 1

    # If tests pass, exit with success
    if test_result.returncode == 0:
        print("Tests passed successfully!")
        return 0

    # Tests failed, extract error message
    error_message = test_result.stderr if test_result.stderr else test_result.stdout
    print(f"Tests failed with error: {error_message}")

    # Create GitHub issue
    issue_number = create_github_issue(test_result.stdout, error_message, repo_path)
    if not issue_number:
        print("Failed to create GitHub issue. Exiting.")
        return 1

    # Trigger OpenHands if not skipped
    if not args.skip_openhands:
        if not trigger_openhands(issue_number, repo_path):
            print("Failed to trigger OpenHands. Exiting.")
            return 1
        print("Workflow completed successfully. OpenHands is now working on fixing the issue.")
    else:
        print("OpenHands triggering skipped. Issue created successfully.")

    return 0


if __name__ == "__main__":
    sys.exit(main())