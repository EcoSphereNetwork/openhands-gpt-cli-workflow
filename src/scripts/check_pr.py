#!/usr/bin/env python3
import subprocess
import sys
import os
import json
import argparse

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Check a PR for test failures')
    parser.add_argument('pr_number', type=str, help='PR number to check')
    return parser.parse_args()

def checkout_pr(pr_number):
    """Checkout the PR branch locally"""
    print(f"Checking out PR #{pr_number}...")
    
    # Fetch the PR
    fetch_result = subprocess.run(
        ['git', 'fetch', 'origin', f'pull/{pr_number}/head:pr-{pr_number}'],
        capture_output=True,
        text=True
    )
    
    if fetch_result.returncode != 0:
        print(f"Error fetching PR: {fetch_result.stderr}")
        return False
    
    # Checkout the PR branch
    checkout_result = subprocess.run(
        ['git', 'checkout', f'pr-{pr_number}'],
        capture_output=True,
        text=True
    )
    
    if checkout_result.returncode != 0:
        print(f"Error checking out PR: {checkout_result.stderr}")
        return False
    
    print(f"Successfully checked out PR #{pr_number}")
    return True

def run_tests():
    """Run local tests and return the result"""
    print("Running tests on PR branch...")
    
    test_result = subprocess.run(
        'npm run test',
        shell=True,
        capture_output=True,
        text=True
    )
    
    return test_result

def comment_on_pr(pr_number, message, success):
    """Add a comment to the PR with test results"""
    print("Adding comment to PR...")
    
    # Set the comment prefix based on success
    prefix = "✅ Tests passed!" if success else "❌ Tests failed!"
    
    comment_body = f"""
{prefix}

## Test Results
{message}
  """
    
    # Add comment using GitHub CLI
    result = subprocess.run(
        ['gh', 'pr', 'comment', pr_number, '--body', comment_body],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Error commenting on PR: {result.stderr}")
        return False
    
    print(f"Successfully commented on PR #{pr_number}")
    return True

def approve_pr(pr_number):
    """Approve the PR if tests pass"""
    print(f"Approving PR #{pr_number}...")
    
    result = subprocess.run(
        ['gh', 'pr', 'review', pr_number, '--approve', '--body', "Automated approval: All tests passed."],
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
    
    # Checkout the PR
    if not checkout_pr(pr_number):
        return 1
    
    # Run tests
    test_result = run_tests()
    
    # Check if tests passed
    tests_passed = test_result.returncode == 0
    
    # Get test output
    test_output = test_result.stdout if tests_passed else test_result.stderr
    
    # Comment on PR with test results
    if not comment_on_pr(pr_number, test_output, tests_passed):
        return 1
    
    # If tests passed, approve the PR
    if tests_passed:
        if not approve_pr(pr_number):
            return 1
        print(f"PR #{pr_number} checked and approved.")
    else:
        print(f"PR #{pr_number} checked but tests failed. Not approved.")
    
    # Return to previous branch
    subprocess.run(['git', 'checkout', '-'], capture_output=True)
    
    return 0 if tests_passed else 1

if __name__ == "__main__":
    sys.exit(main())
