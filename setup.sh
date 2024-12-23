#!/bin/bash

# Update package lists
sudo apt-get update

# Install xclip
sudo apt-get install -y xclip
sudo apt-get install -y xselect

# Optionally, install other dependencies
pip install -r requirements.txt
