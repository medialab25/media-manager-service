#!/bin/bash

# Get current directory and user
WORKDIR=$(pwd)
USER=$(whoami)

# Create service file with actual values
sed "s|%WORKDIR%|$WORKDIR|g; s|%USER%|$USER|g" media-manager.service > media-manager.service.tmp

# Install service for current user
mkdir -p ~/.config/systemd/user/
cp media-manager.service.tmp ~/.config/systemd/user/media-manager.service
rm media-manager.service.tmp

# Reload systemd
systemctl --user daemon-reload

echo "Service installed. To manage the service, use:"
echo "  Start: systemctl --user start media-manager"
echo "  Stop: systemctl --user stop media-manager"
echo "  Status: systemctl --user status media-manager"
echo "  Enable: systemctl --user enable media-manager"
echo "  Logs: journalctl --user -u media-manager -f" 