#!/bin/bash

# Get current directory and user
WORKDIR=$(pwd)
USER=$(whoami)

# Create service file with actual values
sed "s|%WORKDIR%|$WORKDIR|g; s|%USER%|$USER|g" mms.service > mms.service.tmp

# Install service for current user
mkdir -p ~/.config/systemd/user/
cp mms.service.tmp ~/.config/systemd/user/mms.service
rm mms.service.tmp

# Reload systemd
systemctl --user daemon-reload

echo "Service installed. To manage the service, use:"
echo "  Start: systemctl --user start mms"
echo "  Stop: systemctl --user stop mms"
echo "  Status: systemctl --user status mms"
echo "  Enable: systemctl --user enable mms"
echo "  Logs: journalctl --user -u mms -f" 