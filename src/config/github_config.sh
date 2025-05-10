#!/bin/bash

# GitHub Configuration Script
# This script sets up GitHub CLI for the OpenHands workflow

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}GitHub CLI Configuration${NC}"
echo "=========================="

# Check GitHub CLI
if ! command -v gh &> /dev/null; then
    echo -e "${RED}GitHub CLI not found. Please install GitHub CLI.${NC}"
    exit 1
fi

# GitHub Authentication
echo -e "${YELLOW}Authenticating with GitHub...${NC}"
read -p "Do you want to authenticate with a token? (y/n): " use_token

if [ "$use_token" = "y" ]; then
    read -p "Enter your GitHub token: " github_token
    echo "$github_token" | gh auth login --with-token
else
    gh auth login
fi

# Set default repository
echo -e "${YELLOW}Setting default repository...${NC}"
read -p "Enter the repository name (e.g., All-Hands-AI/OpenHands): " repo_name
gh repo set-default "$repo_name"

# Create a label for automated issues
echo -e "${YELLOW}Creating 'fix-me' label for issues...${NC}"
gh label create "fix-me" --color "#ff0000" --description "Issues that need automated fixing" || true

echo -e "${GREEN}GitHub configuration completed!${NC}"
exit 0
