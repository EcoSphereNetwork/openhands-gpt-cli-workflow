#!/usr/bin/env python3
"""
OpenHands API Wrapper

This module provides a Python wrapper for the OpenHands API.
"""

import requests
import json
import time
import os
from typing import Dict, Any, Optional, List, Union


class OpenHandsAPI:
    """Python wrapper for the OpenHands API."""

    def __init__(self, base_url: str = "http://localhost:17244"):
        """Initialize the OpenHands API wrapper.

        Args:
            base_url: Base URL of the OpenHands API
        """
        self.base_url = base_url
        self.tasks_url = f"{base_url}/api/tasks"
        self.status_url = f"{base_url}/api/status"

    def get_status(self) -> Dict[str, Any]:
        """Get the status of the OpenHands server.

        Returns:
            Status information
        """
        response = requests.get(self.status_url)
        response.raise_for_status()
        return response.json()

    def create_task(self, command: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new task.

        Args:
            command: Command to execute
            context: Context for the command

        Returns:
            Task information
        """
        payload = {
            "command": command,
            "context": context
        }

        response = requests.post(self.tasks_url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get information about a task.

        Args:
            task_id: ID of the task

        Returns:
            Task information
        """
        response = requests.get(f"{self.tasks_url}/{task_id}")
        response.raise_for_status()
        return response.json()

    def cancel_task(self, task_id: str) -> Dict[str, Any]:
        """Cancel a task.

        Args:
            task_id: ID of the task

        Returns:
            Task information
        """
        response = requests.post(f"{self.tasks_url}/{task_id}/cancel")
        response.raise_for_status()
        return response.json()

    def list_tasks(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all tasks.

        Args:
            status: Optional status filter

        Returns:
            List of tasks
        """
        params = {}
        if status:
            params["status"] = status

        response = requests.get(self.tasks_url, params=params)
        response.raise_for_status()
        return response.json()

    def fix_issue(self, issue_number: str, repository: str, repo_path: Optional[str] = None) -> Dict[str, Any]:
        """Fix a GitHub issue.

        Args:
            issue_number: Number of the issue
            repository: Repository name (owner/repo)
            repo_path: Optional local path to the repository

        Returns:
            Task information
        """
        context = {
            "issue_number": issue_number,
            "repository": repository
        }

        if repo_path:
            context["repo_path"] = repo_path

        return self.create_task("fix-issue", context)

    def check_pr(self, pr_number: str, repository: str, repo_path: Optional[str] = None) -> Dict[str, Any]:
        """Check a GitHub pull request.

        Args:
            pr_number: Number of the pull request
            repository: Repository name (owner/repo)
            repo_path: Optional local path to the repository

        Returns:
            Task information
        """
        context = {
            "pr_number": pr_number,
            "repository": repository
        }

        if repo_path:
            context["repo_path"] = repo_path

        return self.create_task("check-pr", context)

    def run_tests(self, repository: str, repo_path: str, test_command: Optional[str] = None) -> Dict[str, Any]:
        """Run tests on a repository.

        Args:
            repository: Repository name (owner/repo)
            repo_path: Local path to the repository
            test_command: Optional test command

        Returns:
            Task information
        """
        context = {
            "repository": repository,
            "repo_path": repo_path
        }

        if test_command:
            context["test_command"] = test_command

        return self.create_task("run-tests", context)

    def wait_for_task(self, task_id: str, timeout: int = 300, poll_interval: int = 5) -> Dict[str, Any]:
        """Wait for a task to complete.

        Args:
            task_id: ID of the task
            timeout: Timeout in seconds
            poll_interval: Polling interval in seconds

        Returns:
            Task information
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            task = self.get_task(task_id)
            status = task.get("status")

            if status in ["completed", "failed", "canceled"]:
                return task

            time.sleep(poll_interval)

        # Timeout reached
        raise TimeoutError(f"Timeout waiting for task {task_id} to complete")


# Example usage
if __name__ == "__main__":
    api = OpenHandsAPI()
    
    # Get server status
    status = api.get_status()
    print(f"Server status: {json.dumps(status, indent=2)}")
    
    # List tasks
    tasks = api.list_tasks()
    print(f"Tasks: {json.dumps(tasks, indent=2)}")