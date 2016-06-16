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
			"games")
				echo "Installing games"
				INSTALL_GAMES=true
				;;
			"tex")
				echo "Installing tex"
				INSTALL_TEX=true
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
    if [ $UNAME = "FreeBSD" ]; then
	echo "Found a FreeBSD"
	SYSTEM="freebsd"
	INSTALL="sudo pkg install -y "
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
        "freebsd")
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
    if [ $SYSTEM="freebsd" ]; then
        if [ -f /usr/local/share/fonts/TTF/Envy\ Code\ R.ttf ]; then
            echo "Fonts already installed"
            return 0
	fi
	sudo cp $BASEPATH/data/font/*.ttf /usr/local/share/fonts/TTF
    else
        if [ -f /usr/share/fonts/Envy\ Code\ R.ttf ]; then
            echo "Fonts already installed"
            return 0
        fi
        sudo cp $BASEPATH/data/font/*.ttf /usr/share/fonts
    fi
    fc-cache -f -v
}

function installPrereqs() {
    local packs="xsel git vim" 
    echo "Installing prereqs..."
    case $SYSTEM in
        "ubuntu")
            $INSTALL $packs
            ;;
	"freebsd")
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
    local packs="zsh"
    local linpacks="git-flow zsh-lovers fortunes fortunes-de"
    local bsdpacks="gitflow fortune-mod-ferengi_rules_of_acquisition"
    echo "Installing basics..."
    $INSTALL $packs
    case $SYSTEM in
        "ubuntu")
            $INSTALL $linpacks
            ;;
        "freebsd")
            $INSTALL $bsdpacks
            ;;
        "cygwin")
            ;;
    esac
}

function installZsh() {
	if [ ! -f ~/.zshrc ]; then
		cp $BASEPATH/data/templ/zshrc.$SYSTEM ~/.zshrc    
	fi
	if [ "$SHELL"="`which zsh`" ]; then
	    echo "Zsh already login shell"
	    return 0
	fi
	echo "Setting default shell to zsh"
	chsh -s `which zsh`
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
	if [ ! -L ~/.purple ]; then
		if [ -d ~/.purple ]; then
			mv ~/.purple ~/.purple.orig
		fi
		echo "Creating pidgin configs"
		ln -s $BASEPATH/etc/unix/purple ~/.purple
	fi
	if [ ! -L ~/.config/xfce ]; then
		if [ -d ~/.config/xfce ]; then
			mv ~/.config/xfce ~/.config/xfce.orig
		fi
		echo "Creating xfce configs"
		ln -s $BASEPATH/etc/unix/xfce ~/.config/xfce
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
    local packs="curl npm mc w3m links ncdu htop nmap vim bacula-client"
    local linpacks="synaptic openssh-server dos2unix lshw vim-addon-manager vim-pathogen"
    #local bsdpacks=""
    #local ubuntu_packs=""
    echo "Installing programs..."
    $INSTALL $packs
    case $SYSTEM in
        "ubuntu")
            $INSTALL $linpacks
            ;;
        "freebsd")
            #$INSTALL $bsdpacks
            ;;
        "cygwin")
            ;;
    esac
}

function installXPrograms() {
    local packs="launchy devilspie wmctrl inkscape audacity vlc gimp"
    local extPacks="bogofilter hunspell"
    local linpacks="launchy-plugins launchy-skins doublecmd-gtk vim-gtk gdevilspie retext chromium-browser"
    local linextPacks="owncloud-client hunspell-de-de hunspell-ru hunspell-fr hunspell-es xfce4-eyes-plugin"
    local bsdpacks="doublecmd chromium"
    local bsdextPacks="owncloudclient de-hunspell ru-hunspell fr-hunspell es-hunspell"

#unetbootin sublime
    echo "Installing X11 programs..."

    $INSTALL $packs
    if [ "$DEST" = "host" ]; then
	$INSTALL $extPacks
    fi
    case $SYSTEM in
        "ubuntu")
			$INSTALL $linpacks
			if [ "$DEST" = "host" ]; then
				$INSTALL $linextPacks
			fi
            ;;
        "freebsd")
			$INSTALL $bsdpacks
			if [ "$DEST" = "host" ]; then
				$INSTALL $bsdextPacks
			fi
            ;;
        "cygwin")
            ;;
    esac
}

function installCompilers() {
    local packs="subversion meld cgdb gdb cmake"
    local linpacks="qt5-default"
    local bsdpacks="qt5"

    local python="python3-pyqt5 python3-pyqt5.qtquick python3-pyqt5.qtsql python3-pyqt5.qtsvg python3-numpy python3-psycopg2"

    echo "Installing compilers..."

    $INSTALL $packs
    case $SYSTEM in
        "ubuntu")
            $INSTALL $linpacks
	    $INSTALL $python
            ;;
        "freebsd")
            $INSTALL $bsdpacks
            ;;
        "cygwin")
            ;;
    esac
}

function installTex() {
echo "Test"
	if [ ! "$INSTALL_TEX" = true ]; then
		return 0
	fi
    local packs="texmaker lyx latex2html texstudio latexila"
    local linpacks="texlive-music xfonts-cyrillic"
    local bsdpacks="texlive-full font-cronyx-cyrillic font-misc-cyrillic font-screen-cyrillic xorg-fonts-cyrillic"

    echo "Installing tex..."
    $INSTALL $packs

    case $SYSTEM in
        "ubuntu")
            $INSTALL $linpacks
            ;;
        "freebsd")
            $INSTALL $bsdpacks
            ;;
        "cygwin")
            ;;
    esac
}

function installGames() {
	if [ ! "$INSTALL_GAMES" = true ]; then
		return 0
	fi
    local packs="phalanx xboard crafty supertux supertuxkart"
    local linpacks="pychess "
    local bsdpacks="brutalchess chessx pouetchess" # glchess

    echo "Installing games..."
    $INSTALL $packs
    case $SYSTEM in
        "ubuntu")
            $INSTALL $linpacks
            ;;
        "freebsd")
            $INSTALL $bsdpacks
            ;;
        "cygwin")
            ;;
    esac
}

function installTwitter() {
    if which corebird; then
        echo "Twitter already installed"
        return 0
    fi
    echo "Installing twitter..."
    case $SYSTEM in
        "ubuntu")
	    sudo add-apt-repository ppa:ubuntuhandbook1/corebird
	    sudo apt-get update
	    sudo apt-get install corebird
            ;;
        "freebsd")
            $INSTALL corebird
            ;;
        "cygwin")
            ;;
    esac
}


function installExternals() {
	pushd .
	cd ~/Downloads

	# Keybase
	if ! which keybase; then
		echo "Installing keybase"
		wget https://dist.keybase.io/linux/deb/keybase-latest-amd64.deb
		sudo dpkg -i dpkg -i keybase-latest-amd64.deb
		keybase login
	else
		echo "Keybase already installed"
	fi

	# Sublime
	#if ! which sublime_text_3; then
	if ! which subl; then
		echo "Installing sublime text"
		wget https://download.sublimetext.com/sublime-text_build-3114_amd64.deb
		sudo dpkg -i sublime-text_build-3114_amd64.deb
	else
		echo "Sublime already installed"
	fi

	#if ! which gitkraken; then
	if [ ! -f /usr/share/gitkraken/gitkraken ]; then
		echo "Installing gitkraken"
		wget https://release.gitkraken.com/linux/gitkraken-amd64.deb
		sudo dpkg -i gitkraken-amd64.deb
	else
		echo "gitkraken already installed"
	fi

	if [ ! -d ~/work/qt ]; then
		echo "Installing qt5"
		wget http://download.qt.io/official_releases/online_installers/qt-unified-linux-x64-online.run
		sh -x qt-unified-linux-x64-online.run
	else
		echo "qt5 already installed"
	fi

	popd
}

function cloneSources() {
	pushd .
	mkdir -p ~/work/github
	cd ~/work/github
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
    if [ ! -d Godot ]; then
        echo "Cloning Godot"
        git clone git@github.com:slesa/Godot
        cd Godot && git checkout develop && cd ..
    fi
	if [ ! -d GammaRay ]; then
		git clone https://github.com/KDAB/GammaRay
		#cd GammaRay && mkdir build && cd build && cmake .. && make && cd ../..
	fi
	popd
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
#installPrereqs
#createSshKey
#installBasics
#installDotFiles
#installFonts
#installZsh
#installLinks
#installPrograms
#installXPrograms
#installCompilers
#installTwitter
#installGames
installTex
#installExternals
#installLogin
#cloneSources
echo "Done"
