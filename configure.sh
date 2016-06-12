#!/bin/bash

BASEPATH=~/.dotFiles

function readArguments() {
	for i in "$@" 
	do
		case $i in
			"host")
				echo "Installing for a host"
				DEST="host"
				;;
			"slave")
				echo "Installing for a vm slave"
				DEST="slave"
				;;
		esac
		shift
	done
}

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
	if [ "$SHELL"="`which zsh`" ]; then
	    echo "Zsh already login shell"
		return 0
	fi
    echo "Setting default shell to zsh"
    chsh -s `which zsh`
    if [ ! -f ~/.zshrc ]; then
        cp $BASEPATH/data/templ/zshrc.$SYSTEM ~/.zshrc    
    fi
}

function installLinks() {
#pidgin xfce
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
    if [ ! -L ~/.devilspie ]; then
        echo "Creating devilspie config"
        ln -s $BASEPATH/etc/unix/devilspie ~/.devilspie
    fi

	echo "Creating autostarts"
	if [ ! -d ~/.config/autostart ]; then
		mkdir ~/.config/autostart
	fi

	if [ ! -L ~/.config/autostart/devilspie.desktop ]; then
		ln -s $BASEPATH/etc/unix/autostart/devilspie.desktop ~/.config/autostart/devilspie.desktop
	fi
	if [ ! -L ~/.config/autostart/Pidgin.desktop ]; then
		ln -s $BASEPATH/etc/unix/autostart/Pidgin.desktop ~/.config/autostart/Pidgin.desktop
	fi
	if [ ! -L ~/.config/autostart/Launchy.desktop ]; then
		ln -s $BASEPATH/etc/unix/autostart/Launchy.desktop ~/.config/autostart/Launchy.desktop
	fi
	if [ "$DEST" = "host" ]; then
		echo "Creating host autostarts"
		if [ ! -L ~/.config/autostart/ownCloud.desktop ]; then
			ln -s $BASEPATH/etc/unix/autostart/ownCloud.desktop ~/.config/autostart/ownCloud.desktop
		fi
		if [ ! -L ~/.config/autostart/Twitter.desktop ]; then
			ln -s $BASEPATH/etc/unix/autostart/Twitter.desktop ~/.config/autostart/Twitter.desktop
		fi
		if [ ! -L ~/.config/autostart/Thunderbird.desktop ]; then
			ln -s $BASEPATH/etc/unix/autostart/Thunderbird.desktop ~/.config/autostart/Thunderbird.desktop
		fi
		if [ ! -L ~/.config/autostart/TimeTracker.desktop ]; then
			ln -s $BASEPATH/etc/unix/autostart/TimeTracker.desktop ~/.config/autostart/TimeTracker.desktop
		fi
		if [ ! -L ~/.config/autostart/Skype.desktop ]; then
			ln -s $BASEPATH/etc/unix/autostart/Skype.desktop ~/.config/autostart/Skype.desktop
		fi
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
    local packs="launchy launchy-plugins launchy-skins doublecmd-gtk vim-gtk devilspie gdevilspie wmctrl inkscape audacity vlc gimp retext chromium-browser"
	local extPacks="owncloud-client"

#unetbootin sublime
    #local ubuntu_packs=""
    echo "Installing X11 programs..."

    case $SYSTEM in
        "ubuntu")
            $INSTALL $packs
			if [ "$DEST" = "host" ]; then
				$INSTALL extPacks
			fi
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
    sudo cp $BASEPATH/data/img/StarTrekLogo1920x1080.jpg /usr/share/backgrounds
    sudo chmod +r /usr/share/backgrounds/StarTrekLogo1920x1080.jpg
    sudo sed -i '/background=/c\background=/usr/share/backgrounds/StarTrekLogo1920x1080.jpg' /etc/lightdm/lightdm-gtk-greeter.conf
    sudo sed -i '/#background=/c\background=/usr/share/backgrounds/StarTrekLogo1920x1080.jpg' /etc/lightdm/lightdm-gtk-greeter.conf
}

readArguments $@
if [ -z $DEST ]; then
	echo "Please mention either host or slave"
	exit 1
fi
getSystem
ensureRoot
installPrereqs
createSshKey
installBasics
installDotFiles
installFonts
installZsh
installLinks
installPrograms
installXPrograms
installCompilers
installTwitter
installKeybase
installLogin
echo "Done"
