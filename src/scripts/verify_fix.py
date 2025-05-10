#!/usr/bin/env python3
"""
Verify Fix Script

This script verifies a fix implemented by OpenHands by running tests
and closing the issue if the tests pass.
"""

import subprocess
import requests
import json
import os
import sys
import argparse
from pathlib import Path


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Verify a fix implemented by OpenHands')
    parser.add_argument('issue_number', type=str, help='Issue number to verify')
    parser.add_argument('--repo-path', type=str, default=os.getcwd(),
                        help='Path to the repository')
    parser.add_argument('--test-command', type=str, default='npm test',
                        help='Command to run tests')
    parser.add_argument('--auto-close', action='store_true',
                        help='Automatically close the issue if tests pass')
    return parser.parse_args()


def run_tests(test_command, repo_path):
    """Run tests to verify the fix"""
    print(f"Running tests with command: {test_command}")

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


def comment_on_issue(issue_number, message, success, repo_path):
    """Add a comment to the issue with verification results"""
    print("Adding comment to issue...")

    # Set the comment prefix based on success
    prefix = "✅ Fix verified!" if success else "❌ Fix verification failed!"

    comment_body = f"""
{prefix}

## Verification Results
```
{message}
```

## Next Steps
{
    "Tests have passed and the issue can be closed." if success 
    else "The fix did not resolve the issue. Further investigation is needed."
}
"""

    # Add comment using GitHub CLI
    result = subprocess.run(
        ['gh', 'issue', 'comment', issue_number, '--body', comment_body],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Error commenting on issue: {result.stderr}")
        return False

    print(f"Successfully commented on issue #{issue_number}")
    return True


def close_issue(issue_number, repo_path):
    """Close the issue if tests pass"""
    print(f"Closing issue #{issue_number}...")

    result = subprocess.run(
        ['gh', 'issue', 'close', issue_number, '--comment', "Closing issue: Fix verified and tests are passing."],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Error closing issue: {result.stderr}")
        return False

    print(f"Successfully closed issue #{issue_number}")
    return True


def main():
    # Parse command line arguments
    args = parse_args()
    issue_number = args.issue_number
    repo_path = Path(args.repo_path).resolve()

    # Ensure the repository path exists
    if not repo_path.exists() or not repo_path.is_dir():
        print(f"Error: Repository path {repo_path} does not exist or is not a directory")
        return 1

    # Run tests
    test_result = run_tests(args.test_command, repo_path)
    if test_result is None:
        return 1

    # Check if tests passed
    tests_passed = test_result.returncode == 0

    # Get test output
    test_output = test_result.stdout if test_result.stdout else test_result.stderr

    # Comment on issue with verification results
    if not comment_on_issue(issue_number, test_output, tests_passed, repo_path):
        return 1

    # If tests passed and auto-close is enabled, close the issue
    if tests_passed and args.auto_close:
        if not close_issue(issue_number, repo_path):
            return 1
        print(f"Issue #{issue_number} verified and closed.")
    else:
        status = "passed" if tests_passed else "failed"
        closing = "" if not args.auto_close else " Not closed due to test failures."
        print(f"Issue #{issue_number} verified. Tests {status}.{closing}")

    return 0 if tests_passed else 1


if __name__ == "__main__":
    sys.exit(main())