#!/bin/bash

# update
apt-get update

# Install python, pip
apt-get install python python3 python-pip python3-pip

export LC_ALL=C
# Install needed packages
pip3 install -r requirements.txt

# Move gekkeys to the right folder
mv gekkeys.py /usr/bin/gekkeys.py
chmod +x /usr/bin/gekkeys.py

# Create alias for cli
#echo "alias gekkeys='/usr/bin/gekkeys.py'" >> ~/.bashrc

# Reload bashrc
#source ~/.bashrc
