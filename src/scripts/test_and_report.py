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
