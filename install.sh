#!/bin/bash

# Check if the script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root or with sudo."
   exit 1
fi

# Copy ssd_disp.service to /etc/systemd/system/ and overwrite if it exists
cp -f ./ssd_disp.service /etc/systemd/system/

# Reload systemd manager configuration
systemctl daemon-reload

# Enable and restart the service
systemctl stop ssd_disp.service > /dev/null
systemctl enable ssd_disp.service
systemctl restart ssd_disp.service

# Confirmation message
echo "Systemd service ssd_disp has been reloaded, enabled, and restarted."

