#!/usr/bin/env python3
"""
Dev-Server Installer Script

This script installs and configures the Dev-Server-Workflow on the local host.
It integrates with OpenHands and GPT-CLI to provide a complete workflow.
"""

import os
import sys
import subprocess
import argparse
import json
import time
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger("dev-server-installer")

# Constants
DEV_SERVER_REPO = "https://github.com/EcoSphereNetwork/Dev-Server-Workflow.git"
DEV_SERVER_DIR = os.path.expanduser("~/Dev-Server-Workflow")
DEFAULT_ENV_VARS = {
    "N8N_PORT": "5678",
    "MCP_HUB_PORT": "3000",
    "FRONTEND_PORT": "8080",
    "GRAFANA_PORT": "3001",
    "PROMETHEUS_PORT": "9090",
    "OPENHANDS_API_KEY": "",
    "GITHUB_TOKEN": "",
    "GITLAB_TOKEN": "",
    "OPENPROJECT_API_KEY": "",
}


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Install and configure Dev-Server-Workflow')
    parser.add_argument('--install-dir', type=str, default=DEV_SERVER_DIR,
                        help='Installation directory for Dev-Server-Workflow')
    parser.add_argument('--docker', action='store_true', default=True,
                        help='Use Docker installation (default)')
    parser.add_argument('--no-docker', action='store_false', dest='docker',
                        help='Use direct installation (requires Python 3.8+)')
    parser.add_argument('--start', action='store_true',
                        help='Start services after installation')
    parser.add_argument('--setup-cli', action='store_true',
                        help='Install and setup the Dev-Server CLI')
    parser.add_argument('--env-file', type=str,
                        help='Path to custom .env file')
    parser.add_argument('--components', type=str, default="all",
                        help='Comma-separated list of components to install (default: all)')
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


def clone_repository(install_dir):
    """Clone the Dev-Server-Workflow repository"""
    logger.info(f"Cloning Dev-Server-Workflow repository to {install_dir}")
    
    if os.path.exists(install_dir):
        logger.info(f"Directory {install_dir} already exists")
        
        # Check if it's a git repository
        if os.path.exists(os.path.join(install_dir, ".git")):
            logger.info("Updating existing repository")
            run_command(["git", "pull"], cwd=install_dir)
            return
        
        logger.warning(f"Directory {install_dir} exists but is not a git repository")
        response = input(f"Do you want to delete {install_dir} and clone the repository? (y/n): ")
        if response.lower() != "y":
            logger.error("Aborting installation")
            sys.exit(1)
        
        # Delete the directory
        import shutil
        shutil.rmtree(install_dir)
    
    # Create parent directory if it doesn't exist
    os.makedirs(os.path.dirname(install_dir), exist_ok=True)
    
    # Clone the repository
    run_command(["git", "clone", DEV_SERVER_REPO, install_dir])
    logger.info("Repository cloned successfully")


def create_env_file(install_dir, env_file=None):
    """Create .env file for the Dev-Server-Workflow"""
    logger.info("Creating .env file")
    
    env_path = os.path.join(install_dir, ".env")
    
    # If a custom .env file is provided, copy it
    if env_file and os.path.exists(env_file):
        logger.info(f"Using custom .env file from {env_file}")
        import shutil
        shutil.copy(env_file, env_path)
        return
    
    # Check if .env file already exists
    if os.path.exists(env_path):
        logger.info(f".env file already exists at {env_path}")
        response = input("Do you want to overwrite the existing .env file? (y/n): ")
        if response.lower() != "y":
            logger.info("Keeping existing .env file")
            return
    
    # Create .env file from template
    template_path = os.path.join(install_dir, "src", "env-template")
    if not os.path.exists(template_path):
        logger.warning("env-template not found, creating basic .env file")
        
        # Create basic .env file
        with open(env_path, "w") as f:
            for key, value in DEFAULT_ENV_VARS.items():
                f.write(f"{key}={value}\n")
        
        logger.info(f".env file created at {env_path}")
        logger.warning("Please edit the .env file and fill in the required values")
        return
    
    # Copy template to .env
    import shutil
    shutil.copy(template_path, env_path)
    logger.info(f".env file created from template at {env_path}")
    logger.warning("Please edit the .env file and fill in the required values")


def docker_installation(install_dir, start=False, components="all"):
    """Perform Docker installation of Dev-Server-Workflow"""
    logger.info("Performing Docker installation")
    
    # Check if Docker is installed
    try:
        run_command(["docker", "--version"])
        run_command(["docker-compose", "--version"])
    except Exception:
        logger.error("Docker or Docker Compose not installed")
        logger.info("Please install Docker and Docker Compose and try again")
        sys.exit(1)
    
    # Run docker-start.sh script
    docker_start_script = os.path.join(install_dir, "docker-start.sh")
    
    # Make script executable
    run_command(["chmod", "+x", docker_start_script])
    
    # Show help
    run_command([docker_start_script, "help"])
    
    # Start containers if requested
    if start:
        if components == "all":
            logger.info("Starting all containers")
            run_command([docker_start_script, "start"])
        else:
            logger.info(f"Starting components: {components}")
            run_command([docker_start_script, "start"] + components.split(","))
        
        # Run setup
        logger.info("Running setup")
        run_command([docker_start_script, "setup"])
    
    logger.info("Docker installation completed")
    
    # Print access information
    logger.info("\nAccess the services at:")
    logger.info("- n8n: http://localhost:5678 (admin/password)")
    logger.info("- MCP-Hub: http://localhost:3000")
    logger.info("- Frontend: http://localhost:8080")
    logger.info("- Grafana: http://localhost:3001 (admin/admin)")
    logger.info("- Prometheus: http://localhost:9090")


def direct_installation(install_dir, start=False, components="all"):
    """Perform direct installation of Dev-Server-Workflow"""
    logger.info("Performing direct installation")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        logger.error("Python 3.8+ is required for direct installation")
        logger.info("Please install Python 3.8+ or use Docker installation")
        sys.exit(1)
    
    # Install dependencies
    logger.info("Installing dependencies")
    requirements_file = os.path.join(install_dir, "requirements.txt")
    run_command(["pip", "install", "-r", requirements_file])
    
    # Run setup script
    setup_script = os.path.join(install_dir, "setup.py")
    run_command(["python", setup_script, "install"])
    
    # Start services if requested
    if start:
        if components == "all":
            logger.info("Starting all services")
            run_command(["python", "-m", "src.n8n_setup_main", "start"], cwd=install_dir)
        else:
            logger.info(f"Starting components: {components}")
            run_command(["python", "-m", "src.n8n_setup_main", "start", "--components", components], cwd=install_dir)
    
    logger.info("Direct installation completed")


def setup_cli(install_dir):
    """Install and setup the Dev-Server CLI"""
    logger.info("Setting up Dev-Server CLI")
    
    # Check if CLI is already installed
    try:
        result = run_command(["which", "dev-server"])
        logger.info(f"Dev-Server CLI already installed at {result}")
        return
    except Exception:
        logger.info("Dev-Server CLI not installed, installing now")
    
    # Run install script
    install_script = os.path.join(install_dir, "cli", "install.sh")
    
    # Make script executable
    run_command(["chmod", "+x", install_script])
    
    # Run installation
    run_command(["sudo", install_script])
    
    logger.info("Dev-Server CLI installed successfully")
    logger.info("You can now use 'dev-server' command to manage the Dev-Server-Workflow")


def integrate_with_openhands(install_dir):
    """Integrate Dev-Server-Workflow with OpenHands"""
    logger.info("Integrating Dev-Server-Workflow with OpenHands")
    
    # Check if OpenHands is running
    try:
        import requests
        response = requests.get("http://localhost:17243/api/status")
        if response.status_code == 200:
            logger.info("OpenHands is running")
        else:
            logger.warning("OpenHands API returned non-200 status code")
    except Exception:
        logger.warning("OpenHands API not accessible")
        logger.info("Make sure OpenHands is running on port 17243")
    
    # Create integration directory in OpenHands workspace
    openhands_workspace = os.path.expanduser("~/openhands-workspace")
    integration_dir = os.path.join(openhands_workspace, "dev-server-integration")
    os.makedirs(integration_dir, exist_ok=True)
    
    # Create integration config
    config = {
        "name": "Dev-Server-Workflow",
        "description": "Integration with Dev-Server-Workflow",
        "repository": DEV_SERVER_REPO,
        "local_path": install_dir,
        "commands": {
            "start": f"{install_dir}/docker-start.sh start",
            "stop": f"{install_dir}/docker-start.sh stop",
            "status": f"{install_dir}/docker-start.sh status",
            "logs": f"{install_dir}/docker-start.sh logs",
        }
    }
    
    config_path = os.path.join(integration_dir, "config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    logger.info(f"Integration config created at {config_path}")


def main():
    """Main function"""
    args = parse_args()
    
    # Clone repository
    clone_repository(args.install_dir)
    
    # Create .env file
    create_env_file(args.install_dir, args.env_file)
    
    # Perform installation
    if args.docker:
        docker_installation(args.install_dir, args.start, args.components)
    else:
        direct_installation(args.install_dir, args.start, args.components)
    
    # Setup CLI if requested
    if args.setup_cli:
        setup_cli(args.install_dir)
    
    # Integrate with OpenHands
    integrate_with_openhands(args.install_dir)
    
    logger.info("Installation completed successfully")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())