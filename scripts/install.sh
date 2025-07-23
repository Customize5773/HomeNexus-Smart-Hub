#!/bin/bash
# HomeNexus Smart Hub - Automated Setup Script
# Usage: sudo ./install.sh

# Exit on error and trace
set -e
set -x

# System Configuration
echo "*** Updating System ***"
apt update
apt full-upgrade -y
raspi-config nonint do_i2c 0
raspi-config nonint do_spi 0
raspi-config nonint do_serial 2
raspi-config nonint do_ssh 0
echo "dtoverlay=w1-gpio" >> /boot/config.txt

# Install Core Dependencies
echo "*** Installing Dependencies ***"
apt install -y python3-pip python3-venv i2c-tools git python3-dev libgpiod-dev

# Python Environment Setup
echo "*** Configuring Python Environment ***"
python3 -m venv /opt/homenexus
source /opt/homenexus/bin/activate
pip install --upgrade pip setuptools wheel

# Install Python Packages
echo "*** Installing Python Packages ***"
pip install RPi.GPIO smbus2 Adafruit-GPIO Adafruit-MCP3008 adafruit-circuitpython-ina219 mfrc522 flask

# Repository Setup
echo "*** Cloning Repository ***"
cd /opt
git clone https://github.com/yourusername/HomeNexus-Smart-Hub.git
chown -R pi:pi HomeNexus-Smart-Hub
ln -s /opt/HomeNexus-Smart-Hub /home/pi/HomeNexus

# Service Configuration
echo "*** Configuring System Service ***"
cat > /etc/systemd/system/homenexus.service <<EOL
[Unit]
Description=HomeNexus Smart Hub Service
After=network.target

[Service]
User=pi
WorkingDirectory=/opt/HomeNexus-Smart-Hub/firmware
ExecStart=/opt/homenexus/bin/python main.py
Environment=PYTHONUNBUFFERED=1
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOL

# Enable Services
systemctl daemon-reload
systemctl enable homenexus.service

# Hardware Configuration
echo "*** Configuring Hardware ***"
echo "dtparam=i2c_arm=on" >> /boot/config.txt
echo "dtparam=spi=on" >> /boot/config.txt
echo "enable_uart=1" >> /boot/config.txt

# Final Checks
echo "*** Running Diagnostics ***"
i2cdetect -y 1
ls /dev/ttyAMA0
ls /sys/bus/w1/devices/

echo "*** Setup Complete! ***"
echo "Rebooting in 10 seconds..."
sleep 10
reboot now
