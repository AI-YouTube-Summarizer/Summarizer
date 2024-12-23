#!/bin/bash

# Update package lists
sudo apt-get update

# Install xclip
sudo apt-get install -y xclip

# Optionally, install other dependencies
pip install -r requirements.txt
