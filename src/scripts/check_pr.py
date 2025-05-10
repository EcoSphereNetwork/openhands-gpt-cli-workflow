#!/usr/bin/env python3
"""
Check PR Script

This script checks a pull request for test failures and comments on the PR.
"""

import subprocess
import sys
import os
import json
import argparse
from pathlib import Path


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Check a PR for test failures')
    parser.add_argument('pr_number', type=str, help='PR number to check')
    parser.add_argument('--repo-path', type=str, default=os.getcwd(),
                        help='Path to the repository')
    parser.add_argument('--test-command', type=str, default='npm test',
                        help='Command to run tests')
    parser.add_argument('--auto-approve', action='store_true',
                        help='Automatically approve PR if tests pass')
    return parser.parse_args()


def checkout_pr(pr_number, repo_path):
    """Checkout the PR branch locally"""
    print(f"Checking out PR #{pr_number} in {repo_path}...")

    # Change to the repository directory
    original_dir = os.getcwd()
    os.chdir(repo_path)

    try:
        # Fetch the PR
        fetch_result = subprocess.run(
            ['git', 'fetch', 'origin', f'pull/{pr_number}/head:pr-{pr_number}'],
            capture_output=True,
            text=True
        )

        if fetch_result.returncode != 0:
            print(f"Error fetching PR: {fetch_result.stderr}")
            os.chdir(original_dir)
            return False

        # Checkout the PR branch
        checkout_result = subprocess.run(
            ['git', 'checkout', f'pr-{pr_number}'],
            capture_output=True,
            text=True
        )

        if checkout_result.returncode != 0:
            print(f"Error checking out PR: {checkout_result.stderr}")
            os.chdir(original_dir)
            return False

        print(f"Successfully checked out PR #{pr_number}")
        return True
    except Exception as e:
        print(f"Error during checkout: {e}")
        os.chdir(original_dir)
        return False


def run_tests(test_command, repo_path):
    """Run tests on the PR branch"""
    print(f"Running tests with command: {test_command}")

    # Change to the repository directory if not already there
    original_dir = os.getcwd()
    if original_dir != repo_path:
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
        if original_dir != repo_path:
            os.chdir(original_dir)

        return test_result
    except Exception as e:
        print(f"Error running tests: {e}")
        # Change back to the original directory
        if original_dir != repo_path:
            os.chdir(original_dir)
        return None


def comment_on_pr(pr_number, message, success, repo_path):
    """Add a comment to the PR with test results"""
    print("Adding comment to PR...")

    # Set the comment prefix based on success
    prefix = "✅ Tests passed!" if success else "❌ Tests failed!"

    comment_body = f"""
{prefix}

## Test Results
```
{message}
```
"""

    # Add comment using GitHub CLI
    result = subprocess.run(
        ['gh', 'pr', 'comment', pr_number, '--body', comment_body],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Error commenting on PR: {result.stderr}")
        return False

    print(f"Successfully commented on PR #{pr_number}")
    return True


def approve_pr(pr_number, repo_path):
    """Approve the PR if tests pass"""
    print(f"Approving PR #{pr_number}...")

    result = subprocess.run(
        ['gh', 'pr', 'review', pr_number, '--approve', '--body', "Automated approval: All tests passed."],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Error approving PR: {result.stderr}")
        return False

    print(f"Successfully approved PR #{pr_number}")
    return True


def main():
    # Parse command line arguments
    args = parse_args()
    pr_number = args.pr_number
    repo_path = Path(args.repo_path).resolve()

    # Ensure the repository path exists
    if not repo_path.exists() or not repo_path.is_dir():
        print(f"Error: Repository path {repo_path} does not exist or is not a directory")
        return 1

    # Checkout the PR
    if not checkout_pr(pr_number, repo_path):
        return 1

    # Run tests
    test_result = run_tests(args.test_command, repo_path)
    if test_result is None:
        return 1

    # Check if tests passed
    tests_passed = test_result.returncode == 0

    # Get test output
    test_output = test_result.stdout if test_result.stdout else test_result.stderr

    # Comment on PR with test results
    if not comment_on_pr(pr_number, test_output, tests_passed, repo_path):
        return 1

    # If tests passed and auto-approve is enabled, approve the PR
    if tests_passed and args.auto_approve:
        if not approve_pr(pr_number, repo_path):
            return 1
        print(f"PR #{pr_number} checked and approved.")
    else:
        status = "passed" if tests_passed else "failed"
        approval = "" if not args.auto_approve else " Not approved due to test failures."
        print(f"PR #{pr_number} checked. Tests {status}.{approval}")

    # Return to previous branch
    subprocess.run(['git', 'checkout', '-'], cwd=repo_path, capture_output=True)

    return 0 if tests_passed else 1


if __name__ == "__main__":
    sys.exit(main())