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
        "cygwin")
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
    local packs="git-flow zsh zsh-lovers fortunes fortunes-de"
    echo "Installing basics..."
    case $SYSTEM in
        "ubuntu")
            $INSTALL $packs
            ;;
        "cygwin")
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
    if [ ! -L ~/bin/tools ]; then
        echo "Creating link to tools"
        ln -s $BASEPATH/bin/tools ~/bin/tools
    fi
    if [ ! -L ~/.zsh ]; then
        echo "Creating zsh configs"
        ln -s $BASEPATH/etc/unix/zsh ~/.zsh
    fi
    if [ ! -L ~/.gitconfig ]; then
        echo "Creating git config"
        ln -s $BASEPATH/etc/unix/gitconfig ~/.gitconfig
    fi
    if [ ! -L ~/.vimrc ]; then
        echo "Creating vim config"
        ln -s $BASEPATH/etc/unix/vimrc ~/.vimrc
    fi
    if [ ! -L ~/.config/autostart ]; then
        if [ -d ~/.config/autostart ]; then
            mv ~/.config/autostart ~/.config/autostart.bak
        fi
        echo "Creating autostarts"
        ln -s $BASEPATH/etc/unix/autostart ~/.config/autostart
    fi
}

function installPrograms() {
    local packs="synaptic openssh-server curl npm mc dos2unix w3m links ncdu htop nmap lshw vim vim-addon-manager vim-pathogen"
    #local ubuntu_packs=""
    echo "Installing programs..."

    case $SYSTEM in
        "ubuntu")
            $INSTALL $packs
            #$INSTALL $ubuntu_packs
            ;;
        "cygwin")
            ;;
    esac
}

function installXPrograms() {
    local packs="launchy launchy-plugins launchy-skins doublecmd-gtk vim-gtk devilspie gdevilspie owncloud-client wmctrl inkscape audacity vlc gimp retext chromium-browser"
#unetbootin sublime
    #local ubuntu_packs=""
    echo "Installing X11 programs..."

    case $SYSTEM in
        "ubuntu")
            $INSTALL $packs
            #$INSTALL $ubuntu_packs
            ;;
        "cygwin")
            ;;
    esac
}

function installCompilers() {
    local packs="subversion meld qt5-default cgdb gdb cmake"
#gitkraken qt5
    #local ubuntu_packs=""
    echo "Installing compilers..."

    case $SYSTEM in
        "ubuntu")
            $INSTALL $packs
            #$INSTALL $ubuntu_packs
            ;;
        "cygwin")
            ;;
    esac
}

function installTwitter() {
    local bird=`which corebird`
    if [ -n "$bird" ]; then
        echo "Twitter already installed"
        return 0
    fi
    echo "Installing twitter..."
    sudo add-apt-repository ppa:ubuntuhandbook1/corebird
    sudo apt-get update
    sudo apt-get install corebird
}

function installKeybase() {
    local keyb=`which keybase`
    if [ -n "$keyb" ]; then
        echo "Keybase already installed"
        return 0
    fi
    echo "Installing keybase..."
    sudo ln -s /usr/bin/nodejs /usr/bin/node
    sudo npm install -g keybase-installer
    sudo keybase-installer
    keybase login
}

function cloneSources() {
    mkdir ~/work && cd ~/work
    if [ ! -d Trinity ]; then
        echo "Cloning Trinity"
        git clone git@github.com:slesa/Trinity
        cd Trinity && git checkout develop && cd ..
    fi
    if [ ! -d launchy ]; then
        echo "Cloning launchy"
        git clone git@github.com:slesa/launchy
        cd launchy && git checkout develop && cd ..
    fi
}

function installLogin() {
    if [ -f /usr/share/backgrounds/StarTrekLogo1920x1080.jpg ]; then
        echo "Login logo already installed"
        return 0
    fi
    sudo cp $BASEPATH/data/imgs/StarTrekLogo1920x1080.jpg /usr/hare/backgrounds
    sudo chmod +r /usr/hare/backgrounds/StarTrekLogo1920x1080.jpg
    sudo sed -i '/background=/c\background=/usr/hare/backgrounds/StarTrekLogo1920x1080.jpg'
    sudo sed -i '/#background=/c\background=/usr/hare/backgrounds/StarTrekLogo1920x1080.jpg'
}

getSystem
ensureRoot
#installPrereqs
#createSshKey
#installBasics
#installDotFiles
#installFonts
#installZsh
installLinks
#installPrograms
#installXPrograms
#installCompilers
installTwitter
installKeybase
installLogin
echo "Done"