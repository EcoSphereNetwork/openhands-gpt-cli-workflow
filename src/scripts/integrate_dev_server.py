#!/usr/bin/env python3
"""
Dev-Server Integration Script

This script integrates the Dev-Server-Workflow with OpenHands and GPT-CLI.
It sets up the necessary configuration and starts the workflow loop.
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
logger = logging.getLogger("integrate-dev-server")

# Constants
DEV_SERVER_DIR = os.path.expanduser("~/Dev-Server-Workflow")
OPENHANDS_WORKSPACE = os.path.expanduser("~/openhands-workspace")
OPENHANDS_API_URL = "http://localhost:17244/api/tasks"


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Integrate Dev-Server-Workflow with OpenHands and GPT-CLI')
    parser.add_argument('--install-dir', type=str, default=DEV_SERVER_DIR,
                        help='Installation directory for Dev-Server-Workflow')
    parser.add_argument('--openhands-workspace', type=str, default=OPENHANDS_WORKSPACE,
                        help='OpenHands workspace directory')
    parser.add_argument('--start-workflow-loop', action='store_true',
                        help='Start the workflow loop after integration')
    parser.add_argument('--install-cli', action='store_true',
                        help='Install the Dev-Server CLI')
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


def install_dev_server(install_dir):
    """Install Dev-Server-Workflow"""
    logger.info(f"Installing Dev-Server-Workflow to {install_dir}")
    
    # Run the installer script
    try:
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Run the installer
        run_command([
            "python",
            os.path.join(script_dir, "dev_server_installer.py"),
            "--install-dir", install_dir,
            "--docker",
            "--start"
        ])
        
        logger.info("Dev-Server-Workflow installed successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to install Dev-Server-Workflow: {e}")
        return False


def install_dev_server_cli(install_dir):
    """Install Dev-Server CLI"""
    logger.info("Installing Dev-Server CLI")
    
    try:
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Run the installer
        run_command([
            "python",
            os.path.join(script_dir, "dev_server_installer.py"),
            "--install-dir", install_dir,
            "--setup-cli"
        ])
        
        logger.info("Dev-Server CLI installed successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to install Dev-Server CLI: {e}")
        return False


def setup_openhands_integration(install_dir, openhands_workspace):
    """Set up integration with OpenHands"""
    logger.info("Setting up integration with OpenHands")
    
    # Create integration directory in OpenHands workspace
    integration_dir = os.path.join(openhands_workspace, "dev-server-integration")
    os.makedirs(integration_dir, exist_ok=True)
    
    # Create integration config
    config = {
        "name": "Dev-Server-Workflow",
        "description": "Integration with Dev-Server-Workflow",
        "repository": "https://github.com/EcoSphereNetwork/Dev-Server-Workflow.git",
        "local_path": install_dir,
        "commands": {
            "start": f"{install_dir}/docker-start.sh start",
            "stop": f"{install_dir}/docker-start.sh stop",
            "status": f"{install_dir}/docker-start.sh status",
            "logs": f"{install_dir}/docker-start.sh logs",
        },
        "workflow_loop": {
            "script": os.path.join(os.path.dirname(os.path.abspath(__file__)), "workflow_loop.py"),
            "pid_file": os.path.expanduser("~/workflow_loop.pid"),
            "log_file": os.path.expanduser("~/workflow_loop.log")
        }
    }
    
    # Write config to file
    config_path = os.path.join(integration_dir, "config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    logger.info(f"Integration config created at {config_path}")
    
    # Create OpenHands prompt template
    prompt_template = {
        "name": "dev-server-assistance",
        "description": "Assistance with Dev-Server-Workflow",
        "template": """
You are an AI assistant specialized in helping with the Dev-Server-Workflow.
The Dev-Server-Workflow is a comprehensive system for managing development workflows,
integrating n8n automation, MCP (Message Control Protocol) servers, and AI-assisted tools.

User's request: {prompt}

Please provide detailed assistance, including:
1. Explanation of relevant concepts
2. Step-by-step instructions
3. Command examples
4. Troubleshooting tips

Be thorough, accurate, and helpful.
"""
    }
    
    # Write prompt template to file
    prompt_path = os.path.join(integration_dir, "prompt_template.json")
    with open(prompt_path, "w") as f:
        json.dump(prompt_template, f, indent=2)
    
    logger.info(f"Prompt template created at {prompt_path}")
    
    # Register with OpenHands
    try:
        # Check if OpenHands API is accessible
        import requests
        response = requests.get(f"{OPENHANDS_API_URL}/status")
        
        if response.status_code == 200:
            logger.info("Registering with OpenHands API")
            
            # Register integration
            payload = {
                "command": "register-integration",
                "context": {
                    "name": "dev-server-workflow",
                    "config_path": config_path,
                    "prompt_path": prompt_path
                }
            }
            
            response = requests.post(OPENHANDS_API_URL, json=payload)
            
            if response.status_code == 200:
                logger.info("Registered with OpenHands API")
            else:
                logger.warning(f"Failed to register with OpenHands API: {response.status_code} - {response.text}")
        else:
            logger.warning(f"OpenHands API not accessible: {response.status_code}")
    except Exception as e:
        logger.warning(f"Failed to register with OpenHands API: {e}")
    
    return True


def setup_gpt_cli_integration():
    """Set up integration with GPT-CLI"""
    logger.info("Setting up integration with GPT-CLI")
    
    try:
        # Check if GPT-CLI is installed
        run_command(["gpt", "--version"])
        
        # GPT-CLI is already set up in the gpt.yml file
        logger.info("GPT-CLI integration already set up")
        return True
    except Exception:
        logger.warning("GPT-CLI not installed")
        
        # Try to install GPT-CLI
        try:
            run_command(["pip", "install", "gpt-command-line"])
            logger.info("GPT-CLI installed successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to install GPT-CLI: {e}")
            return False


def start_workflow_loop(install_dir):
    """Start the workflow loop"""
    logger.info("Starting workflow loop")
    
    try:
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Make the script executable
        run_command(["chmod", "+x", os.path.join(script_dir, "start_workflow_loop.sh")])
        
        # Start the workflow loop
        run_command([
            os.path.join(script_dir, "start_workflow_loop.sh"),
            "--install-dir", install_dir
        ])
        
        logger.info("Workflow loop started")
        return True
    except Exception as e:
        logger.error(f"Failed to start workflow loop: {e}")
        return False


def main():
    """Main function"""
    args = parse_args()
    
    # Set log level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Install Dev-Server-Workflow
    if not install_dev_server(args.install_dir):
        logger.error("Failed to install Dev-Server-Workflow")
        return 1
    
    # Install Dev-Server CLI if requested
    if args.install_cli:
        if not install_dev_server_cli(args.install_dir):
            logger.warning("Failed to install Dev-Server CLI")
    
    # Set up integration with OpenHands
    if not setup_openhands_integration(args.install_dir, args.openhands_workspace):
        logger.warning("Failed to set up integration with OpenHands")
    
    # Set up integration with GPT-CLI
    if not setup_gpt_cli_integration():
        logger.warning("Failed to set up integration with GPT-CLI")
    
    # Start workflow loop if requested
    if args.start_workflow_loop:
        if not start_workflow_loop(args.install_dir):
            logger.warning("Failed to start workflow loop")
    
    logger.info("Integration completed successfully")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())