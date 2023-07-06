#!/bin/zsh
echo 'Setting up alias for web3-aio-tools';

# Get current dir
CURRENT_PATH=$(pwd);
SHORT_CUT='web3tools';

# Enable alias work outside zsh env
setopt ALIASES;

# Custom zsh script for our tools

# replace this for oh-my-zsh user 
# DIR=~/.oh-my-zsh/custom/web3-aio.zsh
DIR=~/.zshrc
if [ -d "$DIR" ];
then
    echo "$DIR directory exists."
    echo "Let's create the alias now"
else
	echo "$DIR directory does not exist."
	touch $DIR
	echo "file created."
fi

echo "alias $SHORT_CUT='python3 $CURRENT_PATH/main.py'" > $DIR;

echo "Now you may simply call $SHORT_CUT instead of 'python3 $CURRENT_PATH/main.py' after restarting terminal";

