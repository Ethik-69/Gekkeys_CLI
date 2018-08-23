# Geekkeys

An API to rule them all !  
The ssh keys i mean..

## Installation

Easy !

1. `git clone https://gitlab.com/Ethik69/Gekkeys_CLI.git`
2. `cd Gekkeys_CLI`
3. `sudo chmod +x install.sh`
4. `sudo ./install.sh`

## Configuration

Edit geekkeys config file and fill this fields:  
It'll be... in `~/.config/geekkeys/` maybe...

username = xxxxxxxxx  
stage = xxxxxxxxx  
url = https://xxxxxxxxx  
path_to_key_folder = xxxx/xxxx/xxxx  

## Use

1. Without filling the config file:  
`gekkeys -a action -s stage -u username -p password -d data -U url`
2. With it:  
`gekkeys -a action -p password -d data`

If you want some help:  
geekkeys -h
