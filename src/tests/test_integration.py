#!/usr/bin/env python3
"""
Integration Test Script

This script tests the integration between OpenHands and GPT-CLI.
"""

import os
import sys
import unittest
import subprocess
import requests
import time
from pathlib import Path

# Add the scripts directory to the path
sys.path.append(str(Path(__file__).parent.parent / "scripts"))

# Import the OpenHands API wrapper
from openhands_api import OpenHandsAPI


class TestIntegration(unittest.TestCase):
    """Test the integration between OpenHands and GPT-CLI."""

    def setUp(self):
        """Set up the test environment."""
        # Initialize the OpenHands API
        self.api = OpenHandsAPI()
        
        # Set up test repository path
        self.repo_path = os.environ.get("TEST_REPO_PATH", "/workspace/gpt-cli")
        
        # Ensure the repository exists
        self.assertTrue(Path(self.repo_path).exists(), f"Test repository not found: {self.repo_path}")

    def test_openhands_status(self):
        """Test that OpenHands is running."""
        try:
            status = self.api.get_status()
            self.assertIsNotNone(status)
            self.assertIn("status", status)
            print(f"OpenHands status: {status}")
        except Exception as e:
            self.fail(f"Failed to get OpenHands status: {e}")

    def test_gpt_cli_installed(self):
        """Test that GPT-CLI is installed."""
        try:
            result = subprocess.run(["gpt", "--version"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            print(f"GPT-CLI version: {result.stdout.strip()}")
        except Exception as e:
            self.fail(f"GPT-CLI not installed: {e}")

    def test_github_cli_installed(self):
        """Test that GitHub CLI is installed."""
        try:
            result = subprocess.run(["gh", "--version"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            print(f"GitHub CLI version: {result.stdout.strip()}")
        except Exception as e:
            self.fail(f"GitHub CLI not installed: {e}")

    def test_scripts_executable(self):
        """Test that scripts are executable."""
        scripts_dir = Path(__file__).parent.parent / "scripts"
        for script in scripts_dir.glob("*.py"):
            self.assertTrue(os.access(script, os.X_OK), f"Script not executable: {script}")
        for script in scripts_dir.glob("*.sh"):
            self.assertTrue(os.access(script, os.X_OK), f"Script not executable: {script}")

    def test_docker_running(self):
        """Test that Docker containers are running."""
        try:
            result = subprocess.run(
                ["docker", "ps", "--filter", "name=openhands-gui"],
                capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("openhands-gui", result.stdout)
            print("OpenHands container is running")
        except Exception as e:
            self.fail(f"Failed to check Docker containers: {e}")

    def test_openhands_api_accessible(self):
        """Test that OpenHands API is accessible."""
        try:
            response = requests.get("http://localhost:17243/api/status")
            self.assertEqual(response.status_code, 200)
            print("OpenHands API is accessible")
        except Exception as e:
            self.fail(f"OpenHands API not accessible: {e}")

    def test_create_task(self):
        """Test creating a task in OpenHands."""
        try:
            task = self.api.create_task("echo", {"message": "Hello, World!"})
            self.assertIsNotNone(task)
            self.assertIn("task_id", task)
            print(f"Created task: {task}")
            
            # Wait for the task to complete
            task_id = task["task_id"]
            task_result = self.api.wait_for_task(task_id, timeout=30)
            self.assertEqual(task_result["status"], "completed")
            print(f"Task completed: {task_result}")
        except Exception as e:
            self.fail(f"Failed to create task: {e}")


if __name__ == "__main__":
    unittest.main()