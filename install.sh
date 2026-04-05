#!/bin/bash

echo -e "\033[1;95m═══════════════════════════════════════\033[0m"
echo -e "\033[1;95m     VELIONX BLOOD STRIKE PANEL       \033[0m"
echo -e "\033[1;95m        Installing...                 \033[0m"
echo -e "\033[1;95m═══════════════════════════════════════\033[0m"

# Update packages
echo -e "\033[93m[*] Updating packages...\033[0m"
pkg update -y && pkg upgrade -y

# Install dependencies
echo -e "\033[93m[*] Installing Python & pip...\033[0m"
pkg install python -y

echo -e "\033[93m[*] Installing Flask...\033[0m"
pip install flask

# Download panel
echo -e "\033[93m[*] Downloading VELIONX Panel...\033[0m"
curl -o velionx_panel.py https://raw.githubusercontent.com/velionx/velionx-panel/main/panel.py

# Create alias
echo "alias velionx='python ~/velionx_panel.py'" >> ~/.bashrc

# Create user database
echo -e "\033[93m[*] Creating user database...\033[0m"

# Run panel
echo -e "\033[92m[✓] INSTALLATION COMPLETE!\033[0m"
echo -e "\033[96m[*] Type 'velionx' or 'python velionx_panel.py' to start\033[0m"

sleep 2
python velionx_panel.py