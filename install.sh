#!/bin/bash

# update
apt-get update

# Install python, pip
apt-get install python python3 python-pip python3-pip -y

# In case, maybe... export LC_ALL=C

# Install needed packages
pip3 install -r requirements.txt

# Move geekkeys to the right folder
mv geekkeys.py /usr/bin/geekkeys
chmod +x /usr/bin/geekkeys

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
