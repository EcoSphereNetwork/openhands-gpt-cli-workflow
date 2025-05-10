#!/bin/bash

# Start Workflow Loop
# This script starts the workflow loop as a background service

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Workflow Loop${NC}"
echo "=========================="

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default values
INSTALL_DIR="$HOME/Dev-Server-Workflow"
CHECK_INTERVAL=300
MAX_RETRIES=3
LOG_FILE="$HOME/workflow_loop.log"
PID_FILE="$HOME/workflow_loop.pid"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --install-dir)
            INSTALL_DIR="$2"
            shift
            shift
            ;;
        --check-interval)
            CHECK_INTERVAL="$2"
            shift
            shift
            ;;
        --max-retries)
            MAX_RETRIES="$2"
            shift
            shift
            ;;
        --log-file)
            LOG_FILE="$2"
            shift
            shift
            ;;
        --pid-file)
            PID_FILE="$2"
            shift
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --install-dir DIR     Installation directory for Dev-Server-Workflow (default: $INSTALL_DIR)"
            echo "  --check-interval SEC  Interval between checks in seconds (default: $CHECK_INTERVAL)"
            echo "  --max-retries NUM     Maximum number of retries for failed operations (default: $MAX_RETRIES)"
            echo "  --log-file FILE       Log file (default: $LOG_FILE)"
            echo "  --pid-file FILE       PID file (default: $PID_FILE)"
            echo "  --help                Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $key"
            exit 1
            ;;
    esac
done

# Check if workflow loop is already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null; then
        echo -e "${YELLOW}Workflow loop is already running with PID $PID${NC}"
        echo "To stop it, run: kill $PID"
        exit 0
    else
        echo -e "${YELLOW}PID file exists but process is not running. Removing PID file.${NC}"
        rm "$PID_FILE"
    fi
fi

# Start workflow loop in the background
echo -e "${YELLOW}Starting workflow loop...${NC}"
nohup python "$SCRIPT_DIR/workflow_loop.py" \
    --install-dir "$INSTALL_DIR" \
    --check-interval "$CHECK_INTERVAL" \
    --max-retries "$MAX_RETRIES" \
    --verbose \
    > "$LOG_FILE" 2>&1 &

# Save PID
echo $! > "$PID_FILE"
echo -e "${GREEN}Workflow loop started with PID $(cat "$PID_FILE")${NC}"
echo "Log file: $LOG_FILE"
echo "PID file: $PID_FILE"
echo ""
echo "To stop the workflow loop, run:"
echo "kill $(cat "$PID_FILE")"

exit 0