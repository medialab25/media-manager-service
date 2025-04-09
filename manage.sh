#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running under systemd
if [ -n "$INVOCATION_ID" ]; then
    MODE="systemd"
else
    MODE="direct"
fi

# Function to check if service is running
is_running() {
    if [ "$MODE" = "systemd" ]; then
        systemctl --user is-active --quiet mms
    else
        pgrep -f "python -m src.app" > /dev/null
    fi
}

# Function to show service status
status() {
    if is_running; then
        echo -e "${GREEN}Service is running${NC}"
        if [ "$MODE" = "systemd" ]; then
            systemctl --user status mms --no-pager
        else
            ps aux | grep "python -m src.app" | grep -v grep
        fi
    else
        echo -e "${RED}Service is not running${NC}"
    fi
}

# Function to show logs
logs() {
    if [ "$MODE" = "systemd" ]; then
        journalctl --user -u mms -f
    else
        tail -f nohup.out 2>/dev/null || echo "No log file found. Start the service first."
    fi
}

# Function to restart service
restart() {
    echo -e "${YELLOW}Restarting service...${NC}"
    stop
    sleep 2
    start
}

# Function to stop service
stop() {
    echo -e "${YELLOW}Stopping service...${NC}"
    if [ "$MODE" = "systemd" ]; then
        systemctl --user stop mms
    else
        pkill -f "python -m src.app"
    fi
    status
}

# Function to kill all instances
killall() {
    echo -e "${YELLOW}Killing all service instances...${NC}"
    pkill -9 -f "python -m src.app"
    if [ "$MODE" = "systemd" ]; then
        systemctl --user stop mms
    fi
    echo -e "${GREEN}All instances killed${NC}"
}

# Function to start service
start() {
    echo -e "${YELLOW}Starting service...${NC}"
    if [ "$MODE" = "systemd" ]; then
        systemctl --user start mms
    else
        nohup python -m src.app > nohup.out 2>&1 &
    fi
    status
}

# Function to update code
update() {
    echo -e "${YELLOW}Updating code...${NC}"
    if is_running; then
        stop
    fi
    
    # Pull latest changes
    git pull
    
    # Reinstall dependencies if requirements changed
    if git diff --name-only HEAD@{1} HEAD | grep -q "requirements.txt"; then
        echo -e "${YELLOW}Requirements changed, reinstalling...${NC}"
        pip install -r requirements.txt
    fi
    
    # Reload config if it changed
    if git diff --name-only HEAD@{1} HEAD | grep -q "config.json"; then
        echo -e "${YELLOW}Configuration changed, reloading...${NC}"
    fi
    
    start
}

# Function to show config
config() {
    if [ -f "config.json" ]; then
        cat config.json
    else
        echo -e "${RED}Config file not found${NC}"
    fi
}

# Function to enable/disable service
enable() {
    if [ "$MODE" = "systemd" ]; then
        echo -e "${YELLOW}Enabling service to start on boot...${NC}"
        systemctl --user enable mms
        status
    else
        echo -e "${RED}Enable/disable only available in systemd mode${NC}"
    fi
}

disable() {
    if [ "$MODE" = "systemd" ]; then
        echo -e "${YELLOW}Disabling service from starting on boot...${NC}"
        systemctl --user disable mms
        status
    else
        echo -e "${RED}Enable/disable only available in systemd mode${NC}"
    fi
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
    update)
        update
        ;;
    config)
        config
        ;;
    killall)
        killall
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|enable|disable|update|config|killall}"
        echo "Mode: $MODE"
        exit 1
        ;;
esac 