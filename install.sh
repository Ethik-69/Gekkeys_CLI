#!/bin/bash

# update
apt-get update

# Install python, pip
apt-get install python python3 python-pip python3-pip -y

# In case, maybe... export LC_ALL=C

# Install needed packages
pip3 install -r requirements.txt

# Move gekkeys to the right folder
mv gekkeys.py /usr/bin/gekkeys
chmod +x /usr/bin/gekkeys

# UserData
#!/bin/sh
#apt-get update
#apt-get upgrade -y
#apt-get dist-upgrade -y
#apt-get install git -y
#git clone https://gitlab.com/Ethik69/Gekkeys_CLI.git
#cd Gekkeys_CLI
#chmod +x install.sh
#./install.sh
#cd ..
#rm -r Gekkeys_CLI
