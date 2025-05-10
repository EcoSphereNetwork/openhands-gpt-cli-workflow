#!/usr/bin/env python3
"""
Fix Issue Script

This script triggers OpenHands to fix a GitHub issue.
"""

import subprocess
import requests
import json
import os
import sys
import argparse
from pathlib import Path

# Constants
OPENHANDS_API_URL = "http://localhost:17244/api/tasks"


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Trigger OpenHands to fix an issue')
    parser.add_argument('issue_number', type=str, help='Issue number to fix')
    parser.add_argument('--repo-path', type=str, default=os.getcwd(),
                        help='Path to the repository')
    parser.add_argument('--wait', action='store_true',
                        help='Wait for OpenHands to complete the fix')
    return parser.parse_args()


def get_repo_info(repo_path):
    """Get repository information from git config"""
    try:
        repo_url = subprocess.run(
            ['git', 'config', '--get', 'remote.origin.url'],
            cwd=repo_path,
            capture_output=True,
            text=True
        ).stdout.strip()

        # Extract owner/repo from URL
        if 'github.com' in repo_url:
            parts = repo_url.split('github.com/')[-1].split('/')
            if len(parts) >= 2:
                owner = parts[0]
                repo = parts[1].replace('.git', '')
                return f"{owner}/{repo}"
        
        # Fallback: just return the URL
        return repo_url
    except Exception as e:
        print(f"Error getting repository information: {e}")
        return None


def trigger_openhands(issue_number, repo_path):
    """Trigger OpenHands API to fix the issue"""
    print(f"Triggering OpenHands to fix issue #{issue_number}...")

    # Get repository information
    repo_name = get_repo_info(repo_path)
    if not repo_name:
        print("Failed to get repository information. Exiting.")
        return None

    payload = {
        'command': 'fix-issue',
        'context': {
            'issue_number': issue_number,
            'repository': repo_name,
            'repo_path': str(repo_path)
        }
    }

    try:
        response = requests.post(
            OPENHANDS_API_URL,
            json=payload
        )

        if response.status_code == 200:
            result = response.json()
            print(f"Successfully triggered OpenHands: {result}")
            return result.get('task_id')
        else:
            print(f"Error triggering OpenHands: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Exception while triggering OpenHands: {e}")
        return None


def wait_for_completion(task_id):
    """Wait for OpenHands to complete the task"""
    print(f"Waiting for OpenHands to complete task {task_id}...")

    status_url = f"{OPENHANDS_API_URL}/{task_id}"
    
    while True:
        try:
            response = requests.get(status_url)
            
            if response.status_code == 200:
                result = response.json()
                status = result.get('status')
                
                if status == 'completed':
                    print("Task completed successfully!")
                    return True
                elif status == 'failed':
                    print(f"Task failed: {result.get('error')}")
                    return False
                elif status == 'in_progress':
                    print("Task still in progress... waiting")
                else:
                    print(f"Unknown status: {status}")
                    return False
            else:
                print(f"Error checking task status: {response.status_code} - {response.text}")
                return False
                
            # Wait before checking again
            import time
            time.sleep(5)
            
        except Exception as e:
            print(f"Exception while checking task status: {e}")
            return False


def main():
    # Parse command line arguments
    args = parse_args()
    issue_number = args.issue_number
    repo_path = Path(args.repo_path).resolve()

    # Ensure the repository path exists
    if not repo_path.exists() or not repo_path.is_dir():
        print(f"Error: Repository path {repo_path} does not exist or is not a directory")
        return 1

    # Trigger OpenHands
    task_id = trigger_openhands(issue_number, repo_path)
    if not task_id:
        print("Failed to trigger OpenHands. Exiting.")
        return 1

    # Wait for completion if requested
    if args.wait:
        if not wait_for_completion(task_id):
            print("OpenHands failed to fix the issue. Exiting.")
            return 1
        print("OpenHands successfully fixed the issue!")
    else:
        print(f"OpenHands is working on fixing issue #{issue_number}. Task ID: {task_id}")

    return 0


if __name__ == "__main__":
    sys.exit(main())