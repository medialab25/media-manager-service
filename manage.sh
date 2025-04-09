#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if service is running
is_running() {
    systemctl --user is-active --quiet mms
}

# Function to show service status
status() {
    if is_running; then
        echo -e "${GREEN}Service is running${NC}"
        systemctl --user status mms --no-pager
    else
        echo -e "${RED}Service is not running${NC}"
    fi
}

# Function to show logs
logs() {
    journalctl --user -u mms -f
}

# Function to restart service
restart() {
    echo -e "${YELLOW}Restarting service...${NC}"
    systemctl --user restart mms
    status
}

# Function to stop service
stop() {
    echo -e "${YELLOW}Stopping service...${NC}"
    systemctl --user stop mms
    status
}

# Function to start service
start() {
    echo -e "${YELLOW}Starting service...${NC}"
    systemctl --user start mms
    status
}

# Function to enable/disable service
enable() {
    echo -e "${YELLOW}Enabling service to start on boot...${NC}"
    systemctl --user enable mms
    status
}

disable() {
    echo -e "${YELLOW}Disabling service from starting on boot...${NC}"
    systemctl --user disable mms
    status
}

# Main command handling
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    logs)
        logs
        ;;
    enable)
        enable
        ;;
    disable)
        disable
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|enable|disable}"
        exit 1
        ;;
esac 