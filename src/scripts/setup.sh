#!/bin/bash

# OpenHands Workflow Setup Script
# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}OpenHands Workflow Setup${NC}"
echo "=============================="

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker not found. Please install Docker.${NC}"
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose not found. Please install Docker Compose.${NC}"
    exit 1
fi

# Check GitHub CLI
if ! command -v gh &> /dev/null; then
    echo -e "${RED}GitHub CLI not found. Please install GitHub CLI.${NC}"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 not found. Please install Python 3.${NC}"
    exit 1
fi

# Create required directories
echo -e "${YELLOW}Creating project structure...${NC}"
mkdir -p docker workspace config scripts gpt-cli

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip3 install requests

# Setup GitHub CLI
echo -e "${YELLOW}Setting up GitHub CLI...${NC}"
echo "Please authenticate with GitHub:"
gh auth login

# Configure GitHub CLI
echo -e "${YELLOW}Configuring GitHub CLI...${NC}"
read -p "Enter GitHub repository (e.g., All-Hands-AI/OpenHands): " github_repo
gh repo set-default "$github_repo"

# Copy configuration files to ~/.config/gpt-cli
echo -e "${YELLOW}Configuring gpt-cli...${NC}"
mkdir -p ~/.config/gpt-cli
cp gpt-cli/gpt.yml ~/.config/gpt-cli/

# Make scripts executable
echo -e "${YELLOW}Making scripts executable...${NC}"
chmod +x scripts/test_and_report.py
chmod +x scripts/check_pr.py
chmod +x setup.sh

# Start Docker containers
echo -e "${YELLOW}Starting Docker containers...${NC}"
cd docker && docker-compose up -d
cd ..

echo -e "${GREEN}Setup completed successfully!${NC}"
echo ""
echo "Next steps:"
echo "1. Access OpenHands GUI at http://localhost:3000"
echo "2. In OpenHands GUI, configure GitHub token (Settings → Git Settings)"
echo "3. Run tests with: gpt run-tests"
echo "4. Check PRs with: gpt check-pr <PR_NUMBER>"
echo ""
echo "Enjoy your automated workflow!"

exit 0
