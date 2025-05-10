#!/usr/bin/env python3
"""
Dev-Server CLI Wrapper

This script serves as a wrapper for the Dev-Server CLI, providing integration
with OpenHands and GPT-CLI.
"""

import os
import sys
import subprocess
import argparse
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger("dev-server-cli-wrapper")

# Constants
DEV_SERVER_DIR = os.path.expanduser("~/Dev-Server-Workflow")
OPENHANDS_API_URL = "http://localhost:17243/api/tasks"


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Dev-Server CLI Wrapper')
    parser.add_argument('command', nargs='?', default='help',
                        help='Command to run (default: help)')
    parser.add_argument('args', nargs='*',
                        help='Arguments for the command')
    parser.add_argument('--install-dir', type=str, default=DEV_SERVER_DIR,
                        help='Installation directory for Dev-Server-Workflow')
    parser.add_argument('--use-openhands', action='store_true',
                        help='Use OpenHands for assistance')
    return parser.parse_args()


def run_command(command, cwd=None, shell=False):
    """Run a command and return the result"""
    logger.info(f"Running command: {command}")
    
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


def check_dev_server_installed():
    """Check if Dev-Server CLI is installed"""
    try:
        run_command(["which", "dev-server"])
        return True
    except Exception:
        return False


def install_dev_server_cli(install_dir):
    """Install Dev-Server CLI"""
    logger.info("Installing Dev-Server CLI")
    
    # Check if installation directory exists
    if not os.path.exists(install_dir):
        logger.error(f"Installation directory {install_dir} does not exist")
        logger.info("Please run 'gpt dev-server --install-dir {install_dir}' first")
        return False
    
    # Run install script
    install_script = os.path.join(install_dir, "cli", "install.sh")
    
    # Check if install script exists
    if not os.path.exists(install_script):
        logger.error(f"Install script {install_script} not found")
        return False
    
    # Make script executable
    run_command(["chmod", "+x", install_script])
    
    # Run installation
    try:
        run_command(["sudo", install_script])
        logger.info("Dev-Server CLI installed successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to install Dev-Server CLI: {e}")
        return False


def run_dev_server_command(command, args):
    """Run a Dev-Server CLI command"""
    # Construct the command
    full_command = ["dev-server", command] + args
    
    # Run the command
    try:
        result = subprocess.run(full_command, capture_output=False)
        return result.returncode
    except Exception as e:
        logger.error(f"Failed to run Dev-Server CLI command: {e}")
        return 1


def ask_openhands(prompt):
    """Ask OpenHands for assistance"""
    logger.info(f"Asking OpenHands: {prompt}")
    
    try:
        import requests
        
        # Prepare the payload
        payload = {
            "command": "dev-server-assistance",
            "context": {
                "prompt": prompt,
                "source": "dev-server-cli-wrapper"
            }
        }
        
        # Send the request
        response = requests.post(OPENHANDS_API_URL, json=payload)
        
        # Check the response
        if response.status_code == 200:
            result = response.json()
            logger.info("OpenHands response received")
            return result
        else:
            logger.error(f"OpenHands API returned status code {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Failed to ask OpenHands: {e}")
        return None


def main():
    """Main function"""
    args = parse_args()
    
    # Check if Dev-Server CLI is installed
    if not check_dev_server_installed():
        logger.warning("Dev-Server CLI not installed")
        
        # Ask user if they want to install it
        response = input("Do you want to install Dev-Server CLI? (y/n): ")
        if response.lower() == "y":
            if install_dev_server_cli(args.install_dir):
                logger.info("Dev-Server CLI installed successfully")
            else:
                logger.error("Failed to install Dev-Server CLI")
                return 1
        else:
            logger.error("Dev-Server CLI is required to run this command")
            return 1
    
    # If command is help and OpenHands is available, ask for assistance
    if args.command == "help" and args.use_openhands:
        logger.info("Asking OpenHands for assistance with Dev-Server CLI")
        
        # Construct the prompt
        prompt = "I need help with the Dev-Server CLI. Please provide an overview of available commands and their usage."
        
        # Ask OpenHands
        response = ask_openhands(prompt)
        
        if response:
            # Print the response
            print("\n=== OpenHands Assistance ===\n")
            print(response.get("result", "No response from OpenHands"))
            print("\n===========================\n")
    
    # Run the Dev-Server CLI command
    return run_dev_server_command(args.command, args.args)


if __name__ == "__main__":
    sys.exit(main())