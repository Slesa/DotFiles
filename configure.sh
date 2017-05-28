#!/bin/bash

BASEPATH=~/.dotfiles

### determine if installation is on a host or a virtual machine
### additionally, packages can be turned on and off
function readArguments() {
	if [ -z "$@" ]; then
		echo "Available parameters:"
		echo $0 "[ host|vm ]" 
		echo "  games|nogames  tex|notex" 
	fi
	for i in "$@" 
	do
		case $i in
			"host")
				echo "Installing for a host"
				DEST="host"
				;;
			"vm")
				echo "Installing for a vm slave"
				DEST="slave"
				;;
			"games")
				echo "Installing games"
				INSTALL_GAMES=true
				;;
			"nogames")
				echo "Installing no games"
				INSTALL_GAMES=false
				;;
			"tex")
				echo "Installing tex"
				INSTALL_TEX=true
				;;
		esac
		shift
	done
}

function waitForKey() {
	echo "[Press key to continue]" && read -n 1 -s
}

### determine the running OS. Can be Mac, BSD or Ubuntu
function getSystem() {
	local UNAME=`uname -s`
	echo "Operating system is reported as " $UNAME
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
        if grep -q Microsoft /proc/version; then
		echo "Found an Ubuntu on Windows"
		SYSTEM="wwin10"
		INSTALL="sudo apt-get install -y "
		return 0
	fi	
	local LOC_APT=`which apt`
	if [ $LOC_APT = "/usr/bin/apt" ]; then
		echo "Found an Ubuntu"
		SYSTEM="ubuntu"
		INSTALL="sudo apt-get install -y "
		return 0
	fi
	if [ $LOC_APT = "/usr/local/bin/apt" ]; then
		echo "Found Linux Mint"
		SYSTEM="ubuntu"
		INSTALL="sudo apt-get install -y "
		return 0
	fi
	SYSTEM="unknown"
}

### Copy a string to the clipboard, using OS functions
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
		"win10")
			cat $1 | xsel --clipboard
			;;
		"cygwin")
			echo "$1" > /dev/clipboard
			;;
	esac
}

### Ensure that we have root capabilities
function ensureRoot() {
	if [[ $EUID -ne 0 ]]; then
		echo "Not started as root"
		sudo ls > /dev/null
		return 0
	fi
	echo "We are already root"
}

### We need at least an editor and a source code management
function installPrereqs() {
	local packs="xsel git vim firefox" 
	echo "Installing prereqs..."
	case $SYSTEM in
		"ubuntu")
			$INSTALL $packs
			;;
		"freebsd")
			$INSTALL $packs
			;;
		"win10")
			$INSTALL $packs
			;;
		"cygwin")
			;;
	esac
}

function installOwnCube() {
#    sudo sh -c "echo 'deb http://download.opensuse.org/repositories/isv:/ownCloud:/desktop/Ubuntu_16.10/ /' > /etc/apt/sources.list.d/owncloud-client.list"
#    sudo apt-get update
#    sudo apt-get install owncloud-client
	if [ "$SYSTEM"="win10" ]; then
		return 0
	fi
	local packs="owncloud-client" 
	echo "Installing owncube..."
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
	if [[ "$(pidof owncloud | wc -w)" -eq "0" ]]; then
	echo "Starting owncube..."
	owncloud &
	waitForKey
	fi
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
	waitForKey
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


function installFonts() {
	if [ "$SYSTEM"="win10" ]; then
		return 0
	fi
	echo "Installing fonts..."
	case $SYSTEM in
		"freebsd")
			echo "Fonts for freebsd"
			if [ -f /usr/local/share/fonts/TTF/Envy\ Code\ R.ttf ]; then
				echo "Fonts already installed"
				return 0
			fi
			sudo cp $BASEPATH/data/font/*.ttf /usr/local/share/fonts/TTF
			;;
		"ubuntu"|"cygwin")
			echo "Fonts for non freebsd"
			if [ -f /usr/share/fonts/Envy\ Code\ R.ttf ]; then
				echo "Fonts already installed"
				return 0
			fi
			sudo cp $BASEPATH/data/font/*.ttf /usr/share/fonts
			;;
	esac
	fc-cache -f -v
}

function installBasics() {
	local packs="zsh"
	local linpacks="git-flow zsh-lovers fortunes fortunes-de hfsplus hfsutils"
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
		"win10")
			$INSTALL $linpacks
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

function installPrograms() {
	local packs="curl npm mc w3m links ncdu htop nmap bacula-client tmux"
	local linpacks="synaptic openssh-server dos2unix lshw vim-addon-manager vim-pathogen"
	local bsdpacks="xorg xfce slim slim-themes"
	#local ubuntu_packs=""
	echo "Installing programs..."
	$INSTALL $packs
	case $SYSTEM in
		"ubuntu")
			$INSTALL $linpacks
			;;
		"freebsd")
			$INSTALL $bsdpacks
			if ! grep -q "startxfce4" ~/.xinitrc;  then
				echo '/usr/local/bin/startxfce4' >> ~/.xinitrc
			fi
			if ! grep -q "slim_enable" /etc/rc.conf; then
				echo 'slim_enable="YES"' | sudo tee -a /etc/rc.conf
			fi
			if ! grep -q "dbus_enable" /etc/rc.conf; then
				echo 'dbus_enable="YES"' | sudo tee -a /etc/rc.conf
			fi
				if ! grep -q "hald_enable" /etc/rc.conf; then
				echo 'hald_enable="YES"' | sudo tee -a /etc/rc.conf
			fi
			;;
		"win10")
			$INSTALL $linpacks
			;;
		"cygwin")
			;;
	esac
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
		echo "Creating zsh config"
		ln -s $BASEPATH/etc/unix/zsh ~/.zsh
	fi
	if [ ! -L ~/.tmux.conf ]; then
		echo "Creating tmux config"
		ln -s $BASEPATH/etc/unix/tmux.conf ~/.tmux.conf
	fi
	if [ ! -L ~/.gitconfig ]; then
		echo "Creating git config"
		ln -s $BASEPATH/etc/unix/gitconfig ~/.gitconfig
	fi
	if [ ! -L ~/.vimrc ]; then
		echo "Creating vim config"
		ln -s $BASEPATH/etc/unix/vimrc ~/.vimrc
	fi
	#if [ ! -L ~/.devilspie ]; then
	#    echo "Creating devilspie config"
	#    ln -s $BASEPATH/etc/unix/devilspie ~/.devilspie
	#fi
	#if [ ! -L ~/.purple ]; then
	#    if [ -d ~/.purple ]; then
	#        mv ~/.purple ~/.purple.orig
	#    fi
	#    echo "Creating pidgin configs"
	#    ln -s $BASEPATH/etc/unix/purple ~/.purple
	#fi
	if [ "$SYSTEM"="win10" ]; then
		return 0
	fi
	if [ ! -L ~/launchy.ini ]; then
		echo "Creating launchy config"
		rm ~/launchy.ini
		ln -s $BASEPATH/etc/unix/launchy.ini ~/launchy.ini
	fi

	local autostartSource=$BASEPATH/etc/unix/autostart
	local autostartDir=~/.config/autostart
	if [ ! -d $autostartDir ]; then
		echo "Creating autostarts"
		mkdir $autostartDir
	fi

#    if [ ! -L ~/.config/autostart/devilspie.desktop ]; then
#        ln -s $BASEPATH/etc/unix/autostart/devilspie.desktop ~/.config/autostart/devilspie.desktop
#    fi
#    if [ ! -L ~/.config/autostart/Pidgin.desktop ]; then
#        ln -s $BASEPATH/etc/unix/autostart/Pidgin.desktop ~/.config/autostart/Pidgin.desktop
#    fi
	local autoLaunchyFn=Launchy.desktop
	local autoLaunchyDf=$autostartDir/$autoLaunchyFn
	if [ ! -L $autoLaunchyDf ]; then
		ln -s $autostartSource/$autoLaunchyFn $autoLaunchyDf
	fi
	if [ "$DEST" = "host" ]; then
		local autoOwnCloudFn=ownCloud.desktop
		local autoOwnCloudDf=$autostartDir/$autoOwnCloudFn
		if [ ! -f $autoOwnCloudDf ]; then
			echo "Creating ownCloud autostart"
			ln -s $autostartSource/$autoOwnCloudFn $autoOwnCloudDf
		fi
		local autoTwitterFn=Twitter.desktop
		local autoTwitterDf=$autostartDir/$autoTwitterFn
		if [ ! -L $autoTwitterDf ]; then
			echo "Creating Twitter autostart"
		    ln -s $autostartSource/$autoTwitterFn $autoTwitterDf
		fi
		local autoMailFn=Thunderbird.desktop
		local autoMailFd=$autostartDir/$autoMailFn
		if [ ! -L $autoMailFd ]; then
			echo "Creating Thunderbird autostart"
			ln -s $autostartSource/$autoMailFn $autoMailFd
		fi
		local autoSkypeFn=Skype.desktop
		local autoSkypeDf=$autostartDir/$autoSkypeFn
		if [ ! -L $autoSkypeDf ]; then
			echo "Creating Skype autostart"
			ln -s $autostartSource/$autoSkypeFn $autoSkypeDf
		fi
	fi
}

function installXfceLinks() {

	if [ "$SYSTEM"="win10" ]; then
		return 0
	fi

	local xfceSource=$BASEPATH/etc/unix/xfce4
	local xfceBase=~/.config/xfce4
	local channelBase=$xfceBase/xfconf/xfce-perchannel-xml

	# Filemanager
	local thunarFn=thunar.xml
	local thunarRc=$channelBase/$thunarFn
	if [ ! -L $thunarRc ]; then
		echo "Creating thunar config"
		mv $thunarRc $thunarRc.bak
		ln -s $xfceSource/$thunarFn $thunarRc
	fi

	# Workspaces
	local workspaceFn=xfwm4.xml
	local workspaceRc=$channelBase/$workspaceFn
	if [ ! -L $workspaceRc ]; then
		echo "Creating workspace config"
		mv $workspaceRc $workspaceRc.bak
		ln -s $xfceSource/$workspaceFn $workspaceRc
	fi

	# Keyboard
	local keyboardFn=keyboards.xml
	local keyboardRc=$channelBase/$keyboardFn
	if [ ! -L $keyboardRc ]; then
		echo "Creating keyboard config"
		mv $keyboardRc $keyboardRc.bak
		ln -s $xfceSource/$keyboardFn $keyboardRc
	fi
	local keybLayFn=keyboard-layout.xml
	local keybLayRc=$channelBase/$keybLayFn
	if [ ! -L $keybLayRc ]; then
		echo "Creating keyboard layout config"
		mv $keybLayRc $keybLayRc.bak
		ln -s $xfceSource/$keybLayFn $keybLayRc
	fi

	# Notifications
	local notifyFn=xfce4-notifyd.xml
	local notifyRc=$channelBase/$notifyFn
	if [ ! -L $notifyRc ]; then
		echo "Creating notification config"
		mv $notifyRc $notifyRc.bak
		ln -s $xfceSource/$notifyFn $notifyRc
	fi

	# Terminal
	local terminalFn=terminalrc
	local terminalRc=$xfceBase/terminal/$terminalFn
	if [ ! -L $terminalRc ]; then
		echo "Creating terminal config"
		mv $terminalRc $terminalRc.bak
		ln -s $xfceSource/$terminalFn $terminalRc
	fi

	# Power Manager
	local powerFn=xfce4-power-manager.xml
	local powerRc=$channelBase/$powerFn
	if [ ! -L $powerRc ]; then
		echo "Creating power manager config"
		mv $powerRc $powerRc.bak
		ln -s $xfceSource/$powerFn $powerRc
	fi

	# Keyboard shortcuts
	local shortcutFn=xfce4-keyboard-shortcuts.xml
	local shortcutRc=$channelBase/$shortcutFn
	if [ ! -L $shortcutRc ]; then
		echo "Creating shortcuts config"
		mv $shortcutRc $shortcutRc.bak
		ln -s $xfceSource/$shortcutFn $shortcutRc
	fi

	# Panel
	local panelFn=xfce4-panel.xml
	local panelRc=$channelBase/$panelFn
	if [ ! -L $panelRc ]; then
		echo "Creating panel config"
		mv $panelRc $panelRc.bak
		ln -s $xfceSource/$panelFn $panelRc
	fi
	local panelDn=panel
	local panelDir=$xfceBase/$panelDn
	if [ ! -L $panelDir ]; then
		echo "Creating panel directory"
		mv $panelDir $panelDir.bak
		ln -s $xfceSource/$panelDn $panelDir
	fi

	# Session Manager
	local sessionFn=xfce4-session.xml
	local sessionRc=$channelBase/$sessionFn
	if [ ! -L $sessionRc ]; then
		echo "Creating session manager config"
		mv $sessionRc $sessionRc.bak
		ln -s $xfceSource/$sessionFn $sessionRc
	fi
}


function installXPrograms() {
	if [ "$SYSTEM"="win10" ]; then
		return 0
	fi
	local packs="launchy thunderbird gpgv2 wmctrl inkscape audacity vlc gimp devilspie corebird"
	local extPacks="bogofilter hunspell anki unetbootin"
	local linpacks="launchy-plugins launchy-skins doublecmd-gtk vim-gtk retext chromium-browser gdevilspie"
	local linextPacks="hunspell-de-de hunspell-ru hunspell-fr hunspell-es"
	local bsdpacks="doublecmd chromium"
	local bsdextPacks="owncloudclient de-hunspell ru-hunspell fr-hunspell es-hunspell"

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

function installXfcePrograms() {
	if [ "$SYSTEM"="win10" ]; then
		return 0
	fi
	local linextPacks="xfce4-eyes-plugin"
	local bsdpacks="xfce4-xkb-plugin xfce4-weather-plugin xfce-screenshooter-plugin xfce-cpugraph-plugin"

	local LOC_KWIN=`which kwin`
	if [ "$LOC_KWIN" != "" ]; then
		echo "Probably running on KDE"
	else
	case $SYSTEM in
		"ubuntu")
			#$INSTALL $linpacks
			if [ "$DEST" = "host" ]; then
				$INSTALL $linextPacks
			fi
			;;
		"freebsd")
			$INSTALL $bsdpacks
			#if [ "$DEST" = "host" ]; then
			#    $INSTALL $bsdextPacks
			#fi
			;;
		"cygwin")
			;;
	esac
	fi
}

function installCompilers() {
	if [ "$SYSTEM"="win10" ]; then
		return 0
	fi
	local packs="subversion meld cgdb gdb cmake ccache"
	local linpacks="qt5-default fsharp mono-complete"
	local bsdpacks="qt5"

	#local python="python3-pyqt5 python3-pyqt5.qtquick python3-pyqt5.qtsql python3-pyqt5.qtsvg python3-numpy python3-psycopg2"

	echo "Installing compilers..."

	$INSTALL $packs
	case $SYSTEM in
		"ubuntu")
			$INSTALL $linpacks
			#$INSTALL $python
			;;
		"freebsd")
			$INSTALL $bsdpacks
			;;
		"cygwin")
			;;
	esac
}

function installTex() {
	if [ "$SYSTEM"="win10" ]; then
		return 0
	fi
	if [ ! "$INSTALL_TEX" = true ]; then
		return 0
	fi
	local packs="texmaker lyx latex2html texstudio latexila cjk_latex latex-cjk-japanese t1-cyrillic texlive-lang-cyrillic texlive-fonts-extra"
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
	if [ "$SYSTEM"="win10" ]; then
		return 0
	fi
	if [ ! "$INSTALL_GAMES" = true ]; then
		return 0
	fi
	local packs="phalanx xboard crafty" # supertux supertuxkart
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

#function installTwitter() {
#    if which corebird; then
#        echo "Twitter already installed"
#        return 0
#    fi
#    echo "Installing twitter..."
#    case $SYSTEM in
#        "ubuntu")
#            sudo add-apt-repository ppa:ubuntuhandbook1/corebird
#            sudo apt-get update
#            sudo apt-get install corebird
#            ;;
#        "freebsd")
#            $INSTALL corebird
#            ;;
#        "cygwin")
#            ;;
#    esac
#}


function installExternals() {
	echo "Installing external applications..."
	case $SYSTEM in
		"ubuntu")
			pushd .
			cd ~/Downloads

			# Keybase
			if ! which keybase; then
				echo "Installing keybase"
				curl -O https://prerelease.keybase.io/keybase_amd64.deb
				sudo dpkg -i  keybase_amd64.deb
				sudo apt-get -f install
				run_keybase
			else
				echo "Keybase already installed"
			fi

			# Sublime
			#if ! which sublime_text_3; then
			if ! which subl; then
				echo "Installing sublime text"
				wget https://download.sublimetext.com/sublime-text_build-3114_amd64.deb
				sudo dpkg -i sublime-text_build-3126_amd64.deb
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

			# Visual Studio Code
			if ! which code; then
				echo "Installing VS Code"
				wget -O code_amd64.deb https://go.microsoft.com/fwlink/?LinkID=760868
				sudo dpkg -i `find . -name code_amd64.deb`
				#rm code_amd64.deb
			else    
				echo "VS Code already installed"
			fi

			# Open desktop app
			if ! which opendesktop-app; then
				echo "Installing Open Desktop App"
				$INSTALL libqt5svg5 qml-module-qtquick-controls
				wget https://dl.opendesktop.org/api/files/download/id/1492685474/opendesktop-app_0.1.0-0ubuntu1_amd64.deb
				sudo dpkg -i opendesktop-app*.deb
				#rm opendesktop-app*.deb
			else    
				echo "Open Desktop App already installed"
			fi

			# Skype
			if ! which skype; then
				echo "Installing Skype"
				wget -O skype.deb http://www.skype.com/go/getskype-linux-deb
				sudo dpkg -i skype.deb
				#rm skype.deb
				sudo apt-get -f install
			else
				echo "Skype already installed"
			fi

			if [ ! -d ~/work/qt ]; then
				echo "Installing qt5"
				wget http://download.qt.io/official_releases/online_installers/qt-unified-linux-x64-online.run
				chmod +x qt-unified-linux-x64-online.run
				./qt-unified-linux-x64-online.run &
			else
				echo "qt5 already installed"
			fi

			popd
			;;
		"freebsd")
			$INSTALL keybase linux-sublime3 qt5
			;;
		"cygwin")
			;;
	esac
}

function cloneGithub() {
	local srcpath=~/work/github
	if [ "$SYSTEM"="win10" ]; then
		srcpath=/mnt/c/work/github
	fi
	pushd .
	mkdir -p $srcpath
	cd $srcpath
	if [ ! -d Trinity ]; then
		echo "Cloning Trinity"
		git clone git@github.com:slesa/Trinity
		cd Trinity && git flow init -d && git checkout develop && cd ..
	fi
	if [ ! -d launchy ]; then
		echo "Cloning launchy"
		git clone git@github.com:slesa/launchy
		cd launchy && git flow init -d && git checkout develop && cd ..
	fi
	if [ ! -d Godot ]; then
		echo "Cloning Godot"
		git clone git@github.com:slesa/Godot
	fi
	if [ ! -d fable-react_native-demo ]; then
		echo "Cloning fable-react_native-demo"
		git clone git@github.com:slesa/fable-react_native-demo
		cd fable-react_native-demo && git flow init -d && cd ..
	fi
	if [ ! -d fable-elmish ]; then
		echo "Cloning fable-elmish"
		git clone git@github.com:slesa/fable-elmish
	fi
	if [ ! -d GammaRay ]; then
		git clone https://github.com/KDAB/GammaRay
		#cd GammaRay && mkdir build && cd build && cmake .. && make && cd ../..
	fi
	popd
}

function cloneGitlab() {
	pushd .
	mkdir -p ~/work/gitlab
	cd ~/work/gitlab
	if [ ! -d waiterwatch ]; then
		echo "Cloning waiterwatch"
		git clone git@gitlab.com:slesa/waiterwatch
		cd waiterwatch && git flow init -d && git checkout develop && cd ..
	fi
	popd
}

function installLogin() {
	echo "Installing login logo..."
	case $SYSTEM in
		"ubuntu")
			if [ -f /usr/share/backgrounds/StarTrekLogo1920x1080.jpg ]; then
				echo "Login logo already installed"
				return 0
			fi
			sudo cp $BASEPATH/data/img/StarTrekLogo1920x1080.jpg /usr/share/backgrounds
			sudo chmod +r /usr/share/backgrounds/StarTrekLogo1920x1080.jpg
			sudo sed -i '/background=/c\background=/usr/share/backgrounds/StarTrekLogo1920x1080.jpg' /etc/lightdm/lightdm-gtk-greeter.conf
			sudo sed -i '/#background=/c\background=/usr/share/backgrounds/StarTrekLogo1920x1080.jpg' /etc/lightdm/lightdm-gtk-greeter.conf
			;;
		"freebsd")
			;;
		"cygwin")
			;;
	esac
}


readArguments $@
if [ -z $DEST ]; then
	echo "Please mention either host or vm"
	exit 1
fi
if [ "$SYSTEM" == "unknown" ]; then
	echo "No valid system found"
	exit 1
fi

getSystem
ensureRoot
installPrereqs
installOwnCube
createSshKey
installDotFiles
installFonts
installBasics
installZsh
installPrograms
installLinks
installXfceLinks
installXPrograms
installXfcePrograms
installLogin
installCompilers
installTex
installGames
#installTwitter
cloneGithub
#cloneGitlab
installExternals
echo "Done"
