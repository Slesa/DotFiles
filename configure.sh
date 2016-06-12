#!/bin/bash

BASEPATH=~/.dotFiles

function getSystem() {
    local UNAME=`uname -s`
    if [ $UNAME = "Darwin" ]; then
        echo "Found a Mac"
        SYSTEM="mac"
        return 0
    fi
    local LOC_APT=`which apt`
    if [ $LOC_APT = "/usr/bin/apt" ]; then
        echo "Found an Ubuntu"
        SYSTEM="ubuntu"
	INSTALL="sudo apt-get install -y "
        return 0
    fi
    SYSTEM="unknown"
}

function copyToClipboard() {
    case $SYSTEM in
        "mac")
            pbcopy $1
            ;;
        "ubuntu")
            cat $1 | xsel --clipboard
            ;;
        "cygwin")
            echo "$1" > /dev/clipboard
            ;;
    esac
}

function ensureRoot() {
    if [[ $EUID -ne 0 ]]; then
        echo "Not started as root"
        sudo ls > /dev/null
        return 0
    fi
    echo "We are already root"
}

function createSshKey() {
    if [ -f ~/.ssh/id_rsa.pub ]; then
        echo "SSH key already present"
        return 0
    fi
    echo "Generating SSH key"
    ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -q -N ""
    echo "Add key to github"
    copyToClipboard ~/.ssh/id_rsa.pub
    firefox https://github.com/settings/keys
}

function installFonts() {
    if [ -f /usr/share/fonts/Envy\ Code\ R.ttf ]; then
        echo "Fonts already installed"
        return 0
    fi
    sudo cp $BASEPATH/data/font/*.ttf /usr/share/fonts
    fc-cache -f -v
}

function installPrereqs() {
    local packs="xsel git vim" 
    echo "Installing prereqs..."
    case $SYSTEM in
        "ubuntu")
            $INSTALL $packs
            ;;
    esac
}

function installDotFiles() {
    if [ -d $BASEPATH ]; then
        echo "Dot files already installed"
        cd $BASEPATH
        git pull origin master
        return 0
    fi
    echo "Cloning dot files..."
    git clone git@github.com:slesa/DotFiles $BASEPATH
}

function installBasics() {
    local packs="git-flow zsh zsh-lovers fortune"
    echo "Installing basics..."
    case $SYSTEM in
        "ubuntu")
            $INSTALL $packs
            ;;
    esac
}

function installZsh() {
    echo "Setting default shell to zsh"
    chsh -s `which zsh`
    if [ ! -f ~/.zshrc ]; then
        cp $BASEPATH/data/templ/zshrc.$SYSTEM ~/.zshrc    
    fi
}

function installLinks() {
    if [ ! -d ~/bin ]; then
        echo "Creating local bin directory"
        mkdir ~/bin
    fi
    if [ ! -d ~/bin/tools ]; then
        echo "Creating link to tools"
        ln -s $BASEPATH/bin/tools ~/bin/tools
    fi
    if [ ! -d ~/.zsh ]; then
        echo "Creating zsh configs"
        ln -s $BASEPATH/etc/unix/zsh ~/.zsh
    fi
    if [ ! -f ~/.gitconfig ]; then
        echo "Creating git config"
        ln -s $BASEPATH/etc/unix/gitconfig ~/.gitconfig
    fi
    if [ ! -f ~/.vimrc ]; then
        echo "Creating vim config"
        ln -s $BASEPATH/etc/unix/vimrc ~/.vimrc
    fi
}

#function installPrograms() {
#}

getSystem
#ensureRoot
#installPrereqs
#createSshKey
installBasics
installDotFiles
installFonts
installZsh
installLinks
echo "Done"
