#!/usr/bin/env python3
"""
Workflow Loop

This script implements the workflow loop between OpenHands, GPT-CLI, and Dev-Server-Workflow.
It monitors the Dev-Server-Workflow for issues, triggers OpenHands to fix them,
and uses GPT-CLI to verify the fixes.
"""

import os
import sys
import subprocess
import argparse
import json
import time
import logging
import requests
from pathlib import Path
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("workflow_loop.log")
    ]
)
logger = logging.getLogger("workflow-loop")

# Constants
DEV_SERVER_DIR = os.path.expanduser("~/Dev-Server-Workflow")
OPENHANDS_API_URL = "http://localhost:17243/api/tasks"
CHECK_INTERVAL = 300  # 5 minutes
MAX_RETRIES = 3


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Workflow Loop')
    parser.add_argument('--install-dir', type=str, default=DEV_SERVER_DIR,
                        help='Installation directory for Dev-Server-Workflow')
    parser.add_argument('--check-interval', type=int, default=CHECK_INTERVAL,
                        help='Interval between checks in seconds')
    parser.add_argument('--max-retries', type=int, default=MAX_RETRIES,
                        help='Maximum number of retries for failed operations')
    parser.add_argument('--once', action='store_true',
                        help='Run the workflow loop once and exit')
    parser.add_argument('--verbose', action='store_true',
                        help='Enable verbose logging')
    return parser.parse_args()


def run_command(command, cwd=None, shell=False):
    """Run a command and return the result"""
    logger.debug(f"Running command: {command}")
    
    if isinstance(command, str) and not shell:
        command = command.split()
    
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=shell,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with exit code {e.returncode}")
        logger.error(f"Error output: {e.stderr}")
        raise


def check_dev_server_status(install_dir):
    """Check the status of Dev-Server-Workflow"""
    logger.info("Checking Dev-Server-Workflow status")
    
    try:
        # Run status command
        if os.path.exists(os.path.join(install_dir, "docker-start.sh")):
            status = run_command([os.path.join(install_dir, "docker-start.sh"), "status"])
        else:
            # Try using dev-server CLI
            status = run_command(["dev-server", "status"])
        
        logger.debug(f"Status: {status}")
        return status
    except Exception as e:
        logger.error(f"Failed to check Dev-Server-Workflow status: {e}")
        return None


def get_dev_server_issues(install_dir):
    """Get issues from Dev-Server-Workflow"""
    logger.info("Getting issues from Dev-Server-Workflow")
    
    try:
        # Check if GitHub CLI is installed
        run_command(["gh", "--version"])
        
        # Get issues
        issues = run_command(["gh", "issue", "list", "--repo", "EcoSphereNetwork/Dev-Server-Workflow", "--state", "open", "--json", "number,title,body,labels"])
        
        # Parse JSON
        issues = json.loads(issues)
        
        # Filter issues with "fix-me" label
        fix_me_issues = []
        for issue in issues:
            labels = [label["name"] for label in issue.get("labels", [])]
            if "fix-me" in labels:
                fix_me_issues.append(issue)
        
        logger.info(f"Found {len(fix_me_issues)} issues with 'fix-me' label")
        return fix_me_issues
    except Exception as e:
        logger.error(f"Failed to get Dev-Server-Workflow issues: {e}")
        return []


def trigger_openhands_fix(issue):
    """Trigger OpenHands to fix an issue"""
    logger.info(f"Triggering OpenHands to fix issue #{issue['number']}: {issue['title']}")
    
    try:
        # Prepare the payload
        payload = {
            "command": "fix-issue",
            "context": {
                "issue_number": str(issue["number"]),
                "repository": "EcoSphereNetwork/Dev-Server-Workflow",
                "title": issue["title"],
                "body": issue["body"]
            }
        }
        
        # Send the request
        response = requests.post(OPENHANDS_API_URL, json=payload)
        
        # Check the response
        if response.status_code == 200:
            result = response.json()
            logger.info(f"OpenHands task created: {result.get('task_id')}")
            return result.get("task_id")
        else:
            logger.error(f"OpenHands API returned status code {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Failed to trigger OpenHands fix: {e}")
        return None


def check_openhands_task(task_id):
    """Check the status of an OpenHands task"""
    logger.info(f"Checking OpenHands task {task_id}")
    
    try:
        # Send the request
        response = requests.get(f"{OPENHANDS_API_URL}/{task_id}")
        
        # Check the response
        if response.status_code == 200:
            result = response.json()
            status = result.get("status")
            logger.info(f"OpenHands task status: {status}")
            return status
        else:
            logger.error(f"OpenHands API returned status code {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Failed to check OpenHands task: {e}")
        return None


def verify_fix(issue_number, install_dir):
    """Verify a fix using GPT-CLI"""
    logger.info(f"Verifying fix for issue #{issue_number}")
    
    try:
        # Run verify-fix command
        result = run_command(["gpt", "verify-fix", str(issue_number), "--repo-path", install_dir])
        
        logger.info(f"Verification result: {result}")
        return True
    except Exception as e:
        logger.error(f"Failed to verify fix: {e}")
        return False


def close_issue(issue_number):
    """Close an issue"""
    logger.info(f"Closing issue #{issue_number}")
    
    try:
        # Close the issue
        run_command(["gh", "issue", "close", str(issue_number), "--repo", "EcoSphereNetwork/Dev-Server-Workflow"])
        
        logger.info(f"Issue #{issue_number} closed")
        return True
    except Exception as e:
        logger.error(f"Failed to close issue: {e}")
        return False


def workflow_loop(args):
    """Main workflow loop"""
    logger.info("Starting workflow loop")
    
    while True:
        try:
            # Check Dev-Server-Workflow status
            status = check_dev_server_status(args.install_dir)
            if not status:
                logger.warning("Dev-Server-Workflow status check failed")
            
            # Get issues
            issues = get_dev_server_issues(args.install_dir)
            
            # Process each issue
            for issue in issues:
                issue_number = issue["number"]
                logger.info(f"Processing issue #{issue_number}: {issue['title']}")
                
                # Trigger OpenHands fix
                task_id = trigger_openhands_fix(issue)
                if not task_id:
                    logger.warning(f"Failed to trigger OpenHands fix for issue #{issue_number}")
                    continue
                
                # Wait for OpenHands to complete the task
                retries = 0
                while retries < args.max_retries:
                    # Wait for a while
                    time.sleep(60)  # Wait 1 minute
                    
                    # Check task status
                    status = check_openhands_task(task_id)
                    
                    if status == "completed":
                        logger.info(f"OpenHands task completed for issue #{issue_number}")
                        
                        # Verify the fix
                        if verify_fix(issue_number, args.install_dir):
                            # Close the issue
                            close_issue(issue_number)
                        
                        break
                    elif status == "failed":
                        logger.warning(f"OpenHands task failed for issue #{issue_number}")
                        break
                    elif status == "in_progress":
                        logger.info(f"OpenHands task still in progress for issue #{issue_number}")
                    else:
                        logger.warning(f"Unknown task status: {status}")
                    
                    retries += 1
                
                if retries >= args.max_retries:
                    logger.warning(f"Max retries reached for issue #{issue_number}")
            
            # Exit if running once
            if args.once:
                logger.info("Exiting after one iteration")
                break
            
            # Wait for next check
            logger.info(f"Waiting {args.check_interval} seconds until next check")
            time.sleep(args.check_interval)
        
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received, exiting")
            break
        except Exception as e:
            logger.error(f"Error in workflow loop: {e}")
            logger.info(f"Waiting {args.check_interval} seconds until next check")
            time.sleep(args.check_interval)
    
    logger.info("Workflow loop ended")


def main():
    """Main function"""
    args = parse_args()
    
    # Set log level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Run the workflow loop
    workflow_loop(args)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())