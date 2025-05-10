#!/usr/bin/env python3
import subprocess
import requests
import json
import os
import sys
import time

def run_tests():
    """Run local tests and return the result"""
    print("Running tests...")
    
    test_result = subprocess.run(
        'npm run test',
        shell=True,
        capture_output=True,
        text=True
    )
    
    return test_result

def create_github_issue(test_output, error_message):
    """Create a GitHub issue with test failure details"""
    print("Creating GitHub issue...")
    
    # Format the issue body
    issue_body = f"""
## Test Failure
{error_message}
## Full Test Output
{test_output}
## Metadata
- **Label**: fix-me
- **Priority**: high
- **Run ID**: {time.strftime('%Y%m%d%H%M%S')}
"""

    # Create the issue using GitHub CLI
    result = subprocess.run(
        ['gh', 'issue', 'create', 
         '--title', 'Test Failure: Automated Report', 
         '--body', issue_body,
         '--label', 'fix-me'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Error creating GitHub issue: {result.stderr}")
        return None
    
    # Extract issue number from the result
    # GitHub CLI normally returns the URL to the created issue
    issue_url = result.stdout.strip()
    issue_number = issue_url.split('/')[-1]
    
    print(f"Created issue #{issue_number}: {issue_url}")
    return issue_number

def trigger_openhands(issue_number):
    """Trigger OpenHands API to fix the issue"""
    print(f"Triggering OpenHands to fix issue #{issue_number}...")
    
    payload = {
        'command': 'fix-test-errors',
        'context': {
            'issue_number': issue_number,
            'repository': os.environ.get('GITHUB_REPOSITORY', 'All-Hands-AI/OpenHands')
        }
    }
    
    try:
        response = requests.post(
            'http://localhost:17243/api/tasks',  # Aktualisierter Port
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
    # Run the tests
    test_result = run_tests()
    
    # If tests pass, exit with success
    if test_result.returncode == 0:
        print("Tests passed successfully!")
        return 0
    
    # Tests failed, extract error message
    error_message = test_result.stderr if test_result.stderr else test_result.stdout
    print(f"Tests failed with error: {error_message}")
    
    # Create GitHub issue
    issue_number = create_github_issue(test_result.stdout, error_message)
    if not issue_number:
        print("Failed to create GitHub issue. Exiting.")
        return 1
    
    # Trigger OpenHands
    if not trigger_openhands(issue_number):
        print("Failed to trigger OpenHands. Exiting.")
        return 1
    
    print("Workflow completed successfully. OpenHands is now working on fixing the issue.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
