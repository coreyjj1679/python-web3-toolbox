#!/usr/bin/env bash
echo 'Setting up alias for web3-aio-tools';

# Get current dir
CURRENT_PATH=$(pwd);
SHORT_CUT='web3tools';

# Enable alias work outside zsh env
SHOPT -s expand-aliases;

echo "Removing old alias..."
sed -i ".bak" '/alias web3tools/d' ~/.bashrc

alias $SHORT_CUT='PYTHONPATH=$CURRENT_PATH python3 $CURRENT_PATH/src/cli/main.py'

echo "Now you may simply call $SHORT_CUT instead of 'python3 $CURRENT_PATH/src/cli/main.py'";
