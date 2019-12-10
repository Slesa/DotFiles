#!/bin/bash
# V 0.1
# External in SuSE:
# - fsharp
# - Login screen
# - Qt5
# - GitKraken
# - Skype
# - Rider
# - PyCharm
# - Steam


BASEPATH=~/.dotfiles
ERR='\033[0;31m'
OK='\033[0;32m'
YEL='\033[0;33m'
NC='\033[0m'
TC='\033[0;33m'
HEAD='\033[0;35m'

SUDO="sudo"

I_ARGS=true
I_FULL=false
I_CORE=false
I_OWNCUBE=false
I_SSHKEYS=false
I_DOTFILES=false
I_FONTS=false
I_BASICS=false
I_ZSH=false
I_PROGRAMS=false
I_LINKS=false
I_XPROGS=false
I_COMPS=false
I_LOGIN=false
I_TEX=false
I_GAMES=false
I_GH=false
I_GL=false
I_EXT=false
NO_QT=false
NO_RIDER=false
NO_CHARM=false
NO_SKYPE=false


### ----------------------------------------------------------------------------------------------
### Helper functions
### ----------------------------------------------------------------------------------------------

function waitForKey() {
	echo "[Press key to continue]" && read -n 1 -s
}

function printHelp() {
	echo ""
	echo "Syntax"
	echo ""
	echo -n $0 "[ full ] [core|nocore] [owncube|noowncube] [sshkeys|nosshkeys] [dotfiles|nodotfiles] " 
	echo -n "[fonts|nofonts] [basics|nobasics] [zsh|nozsh] [progs|noprogs] [links|nolinks] [xprogs|noxprogs] " 
	echo -n "[comps|nocomps] [login|nologin] [tex|notex] [games|nogames] [gh|nogh] [gl|nogl] [ext|noext] " 
	echo "[noqt] [norider] [nocharm]"
	echo ""
}


### determine if installation is on a host or a virtual machine
### additionally, packages can be turned on and off
### [X] Cygwin   [ ] Mac   [ ] Linux   [X] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [0.1] SuSE
function readArguments() {
	INSTALL_PREREQS=true
	echo -n "Determine arguments..."
	if [ $SYSTEM == "cygwin" ]; then
		echo -e "${TC}not necessary${NC}"
		INSTALL_GAMES=false
		INSTALL_TEX=false
		INSTALL_OWNCUBE=true
		INSTALL_SSHKEYS=true
		INSTALL_PROGRAMS=true
		INSTALL_XPROGRAMS=true
		SUDO=""
		return 0
	fi
	if [ $# -eq 0 ]; then
		echo -e "${ERR}Missing argument!${NC}"
		I_ARGS=false
		return 1
	fi
	echo ""
	for i in "$@" 
	do
		case $i in
			"full")
				echo "* Full installing"
				I_CORE=true
				I_OWNCUBE=true
				I_SSHKEYS=true
				I_DOTFILES=true
				I_FONTS=true
				I_BASICS=true
				I_ZSH=true
				I_PROGS=true
				I_LINKS=true
				I_XPROGS=true
				I_COMPS=true
				I_LOGIN=true
				I_TEX=true
				I_GAMES=true
				I_GH=true
				I_GL=true
				I_EXT=true
				;;
			"core")
				echo "* Core installation"
				I_CORE=true
				;;
			"nocore")
				echo "* No core installation"
				I_CORE=false
				;;
			"owncube")
				echo "* Owncube installaton"
				I_OWNCUBE=true
				;;
			"noowncube")
				echo "* No owncube installaton"
				I_OWNCUBE=false
				;;
			"sshkeys")
				echo "* Ssh keys installation"
				I_SSHKEYS=true
				;;
			"nosshkeys")
				echo "* No ssh keys installation"
				unset I_SSHKEYS
				;;
			"dotfiles")
				echo "* Dotfiles installation"
				I_DOTFILES=true
				;;
			"nodotfiles")
				echo "* No dotfiles installation"
				unset I_DOTFILES
				;;
			"fonts")
				echo "* Font installation"
				I_FONTS=true
				;;
			"nofonts")
				echo "* No font installation"
				unset I_FONTS
				;;
			"basics")
				echo "* Basics installation"
				I_BASICS=true
				;;
			"nobasics")
				echo "* No basics installation"
				unset I_BASICS
				;;
			"zsh")
				echo "* Zsh installation"
				I_ZSH=true
				;;
			"nozsh")
				echo "* No zsh installation"
				unset I_ZSH
				;;
			"progs")
				echo "* Program installation"
				I_PROGS=true
				;;
			"noprogs")
				echo "* No program installation"
				unset I_PROGS
				;;
			"links")
				echo "* Symbolic links"
				I_LINKS=true
				;;
			"nolinks")
				echo "* No symbolic links"
				unset I_LINKS
				;;
			"xprogs")
				echo "* X Program installation"
				I_XPROGS=true
				;;
			"noxprogs")
				echo "* No X Program installation"
				unset I_XPROGS
				;;
			"comps")
				echo "* Compiler installation"
				I_COMPS=true
				;;
			"nocomps")
				echo "* No compiler installation"
				unset I_COMPS
				;;
			"login")
				echo "* Login wallpaper installation"
				I_LOGIN=true
				;;
			"nologin")
				echo "* No login wallpaper installation"
				unset I_LOGIN
				;;
			"tex")
				echo "* TeX installation"
				I_TEX=true
				;;
			"notex")
				echo "* No TeX installation"
				unset I_TEX
				;;
			"games")
				echo "* Games installation"
				I_GAMES=true
				;;
			"nogames")
				echo "* No games installation"
				unset I_GAMES
				;;
			"gh")
				echo "* Github cloning"
				I_GH=true
				;;
			"nogh")
				echo "* No github cloning"
				unset I_GH
				;;
			"gl")
				echo "* Gitlib cloning"
				I_GL=true
				;;
			"nogl")
				echo "* No githlib cloning"
				unset I_GL
				;;
			"ext")
				echo "* External installation"
				I_EXT=true
				;;
			"noext")
				echo "* No external installation"
				unset I_EXT
				;;
			"noqt")
				echo "* No Qt installation"
				NO_QT=true
				;;
			"norider")
				echo "* No Rider installation"
				NO_RIDER=true
				;;
			"nocharm")
				echo "* No PyCharm installation"
				NO_CHARM=true
				;;
			"noskype")
				echo "* No Skype installation"
				NO_SKYPE=true
				;;

			*)
				echo -e "${ERR}Unknown argument!${NC}"
				I_ARGS=false
				return 2
				;;
		esac
		shift
	done
	echo ""
}

### determine the running OS. Can be Mac, BSD or Ubuntu/Manjaro
### [ ] Cygwin   [ ] Mac   [ ] Linux   [ ] FreeBSD   [ ] LinuxOnWin  [ ] Manjaro  [0.1] SuSE
function getSystem() {
	local UNAME=`uname -s`
	echo "Operating system is reported as " $UNAME
	echo -n "Determine system..."
    if [ $UNAME == CYGWIN* ]; then
		echo -e "${OK}a cygwin system${NC}"
		SYSTEM="cygwin"
		return 0
	fi
	if [ $UNAME = "Darwin" ]; then
		echo -e "${OK}as a Mac${NC}"
		SYSTEM="mac"
		return 0
	fi
	if [ $UNAME = "FreeBSD" ]; then
		echo -e "${OK} as a FreeBSD${NC}"
		SYSTEM="freebsd"
		INSTALL="sudo pkg install -y "
		return 0
	fi
        if grep -q Microsoft /proc/version; then
		echo -e "${OK}as Ubuntu on Windows${NC}"
		SYSTEM="win10"
		INSTALL="sudo apt-get install -y "
		return 0
	fi	
	local LOC_YUM=`which yum 2>/dev/null`
	if [ "$LOC_YUM" = "/usr/bin/yum" ]; then
		echo -e "${OK}as an Fedora${NC}"
		SYSTEM="fedora"
		INSTALL="sudo yum install -y "
		return 0
	fi
	local LOC_ZYP=`which zypper 2>/dev/null`
	if [ "$LOC_ZYP" = "/usr/bin/zypper" ]; then
		echo -e "${OK}as an SuSE${NC}"
		SYSTEM="suse"
		INSTALL="sudo zypper install -ly "
		return 1
	fi
	local LOC_PAC=`which pacman 2>/dev/null`
	if [ "$LOC_PAC" = "/usr/bin/pacman" ]; then
		echo -e "${OK}as an ArchLinux${NC}"
		SYSTEM="arch"
		INSTALL="sudo pacman --noconfirm -Syu "
		INSTALL2="yaourt --noconfirm -S "
		return 0
	fi
	local LOC_APT=`which apt 2>/dev/null`
	if [ "$LOC_APT" = "/usr/bin/apt" ]; then
		echo -e "${OK}as an Ubuntu${NC}"
		SYSTEM="ubuntu"
		INSTALL="sudo apt-get install -y "
		return 0
	fi
	if [ "$LOC_APT" = "/usr/local/bin/apt" ]; then
		echo -e "${OK}as  Linux Mint${NC}"
		SYSTEM="ubuntu"
		INSTALL="sudo apt-get install -y "
		return 0
	fi
	SYSTEM="unknown"
}

### Copy a string to the clipboard, using OS functions
### [ ] Cygwin   [ ] Mac   [ ] Linux   [-] FreeBSD   [ ] LinuxOnWin  [ ] Manjaro  [0.1] SuSE
function copyToClipboard() {
	echo -n "Copy to clipboard "
	case $SYSTEM in
		"mac")
			pbcopy $1
			;;
		"fedora"|"suse"|"ubuntu")
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
	echo -e "${OK}ok${NC}"
}

### Ensure that we have root capabilities
### [X] Cygwin   [ ] Mac   [ ] Linux   [X] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [0.1] SuSE
function ensureRoot() {
	echo -n "Ensure root access..."
    if [ $SYSTEM == "cygwin" ]; then
		echo -e "${TC}not necessary${NC}"
		return 0
    fi
	if [[ $EUID -ne 0 ]]; then
		echo -e "${ERR}not started as root${NC}"
		sudo ls > /dev/null
		return 0
	fi
	echo -e "${OK}ok${NC}"
}



### ----------------------------------------------------------------------------------------------
### Installations
### ----------------------------------------------------------------------------------------------

### We need at least an editor and a source code management
### [X] Cygwin   [ ] Mac   [ ] Linux   [X] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [0.1] SuSE
function installCore() {
	if [ ! "$I_CORE" = true ]; then
		echo -e "${TC}No core packages${NC}"
		return 0
	fi
	local packs="xsel git" 
	local archpacks="yaourt firefox" 
	local noarchpacks="vim firefox" 
	local bsdPacks="pidof firefox" 
	echo -n "Installing core packages..."
	case $SYSTEM in
		"arch")
			$INSTALL $packs $archpacks
			;;
		"suse"|"fedora")
			$INSTALL $packs
			;;
		"ubuntu")
			$INSTALL $packs $noarchpacks
			;;
		"freebsd")
			$INSTALL $packs $noarchpacks $bsdPacks
			;;
		"win10")
			$INSTALL $packs $noarchpacks
			;;
		"cygwin")
			;;
	esac
	echo -e "${OK}ok${NC}"
}

### [X] Cygwin   [ ] Mac   [ ] Linux   [X] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [0.1] SuSE
function installOwnCube() {
#    sudo sh -c "echo 'deb http://download.opensuse.org/repositories/isv:/ownCloud:/desktop/Ubuntu_16.10/ /' > /etc/apt/sources.list.d/owncloud-client.list"
#    sudo apt-get update
#    sudo apt-get install owncloud-client
	if [ ! "$I_OWNCUBE" = true ]; then
		echo -e "${TC}No owncube${NC}"
		return 0
	fi
	echo -n "Installing owncube..."
	if [[ ("$SYSTEM" == "win10") || ("$SYSTEM" == "cygwin")  ]]; then
		echo -e "${TC}not necessary${NC}"
		return 0
	fi
	case $SYSTEM in
		"arch"|"suse"|"ubuntu"|"fedora")
			$INSTALL "owncloud-client"
			;;
		"freebsd")
			$INSTALL "owncloudclient"
			;;
	esac
	echo -e "${OK}ok${NC}"
	if [[ "$(pidof owncloud | wc -w)" -eq "0" ]]; then
		echo "Starting owncube..."
		owncloud &
		# echo "[Waiting for a key]"
		# waitForKey
		echo -e "${OK}ok${NC}"
	fi
}


### [X] Cygwin   [ ] Mac   [ ] Linux   [X] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [0.1] SuSE
function createSshKey() {
	if [ ! "$I_SSHKEYS" = true ]; then
		echo -e "${TC}No ssh keys${NC}"
		return 0
	fi
	echo -n "Creating ssh key..."
	if [ -f ~/.ssh/id_rsa.pub ]; then
		echo -e "${TC}SSH key already present${NC}"
		return 0
	fi
	echo -n "Generating..."
	ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -q -N ""
	echo -n "Add key to github..."
	copyToClipboard ~/.ssh/id_rsa.pub
	firefox https://github.com/settings/keys
	waitForKey
	echo -e "${OK}ok${NC}"
}


### [X] Cygwin   [ ] Mac   [ ] Linux   [X] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [0.1] SuSE
function installDotFiles() {
	if [ ! "$I_DOTFILES" = true ]; then
		echo -e "${TC}No dotfiles${NC}"
		return 0
	fi
	echo -n "Installing dot files..."
	if [ -d $BASEPATH ]; then
		echo -e "${TC}Dot files already installed${NC}"
		cd $BASEPATH
		git pull origin master
		return 0
	fi
	echo -n "Cloning dot files..."
	git clone git@github.com:slesa/DotFiles $BASEPATH
	echo -e "${OK}ok${NC}"
}


### [X] Cygwin   [ ] Mac   [ ] Linux   [ ] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [0.1] SuSE
function installFonts() {
	if [ ! "$I_FONTS" = true ]; then
		echo -e "${TC}No fonts${NC}"
		return 0
	fi
	echo -n "Installing fonts for $SYSTEM..."
	if [ $SYSTEM == "win10" ]; then
		echo -e "${TC}Not necessary${NC}"
		return 0
	fi
	case $SYSTEM in
		"freebsd")
			echo -n "Fonts for freebsd..."
			if [ -f /usr/local/share/fonts/TTF/Envy\ Code\ R.ttf ]; then
				echo -e "${TC}Fonts already installed${NC}"
				return 0
			fi
			sudo cp $BASEPATH/data/font/*.ttf /usr/local/share/fonts/TTF
			;;
		"ubuntu"|"arch"|"cygwin"|"suse"|"fedora")
			echo -n "Fonts for non freebsd..."
			if [ -f /usr/share/fonts/Envy\ Code\ R.ttf ]; then
				echo -e "${TC}Fonts already installed${NC}"
				return 0
			fi
			$SUDO cp $BASEPATH/data/font/*.ttf /usr/share/fonts
			;;
	esac
	fc-cache -f -v
	echo -e "${OK}ok${NC}"
}


### [X] Cygwin   [ ] Mac   [ ] Linux   [X] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [0.1] SuSE
function installBasics() {
	if [ ! "$I_BASICS" = true ]; then
		echo -e "${TC}No basics${NC}"
		return 0
	fi
	echo -n "Installing basics..."
	if [ $SYSTEM == "cygwin" ]; then
		echo -e "${TC}Not necessary${NC}"
		return 0
	fi
	local packs="zsh"
	local fedorapacks="fortune-mod hfsutils gitflow zsh-lovers openconnect rdesktop gcc-c++ synergy"
	local susepacks="fortune hfsutils synergy qsynergy openconnect rdesktop gcc-c++ gcc git-flow"
	local archpacks="synergy fortune-mod zsh-lovers"
	local linpacks="git-flow zsh-lovers fortunes fortunes-de hfsplus hfsutils"
	local bsdpacks="gitflow fortune-mod-bofh pstree inxi synergy"
	$INSTALL $packs
	case $SYSTEM in
		"arch")
			$INSTALL $archpacks
			if ! which git-flow; then
				$INSTALL2 gitflow-avh
			else
				echo "git flow already installed"
			fi
			;;
		"fedora")
			$INSTALL http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-30.noarch.rpm http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-30.noarch.rpm
			$INSTALL $fedorapacks
			;;
		"suse")
			$SUDO zypper ar https://download.opensuse.org/repositories/devel:tools:scm/openSUSE_Tumbleweed/devel:tools:scm.repo 2>/dev/null
			$SUDO zypper refresh
			$INSTALL $susepacks
			;;
		"ubuntu")
			$INSTALL $linpacks
			;;
		"freebsd")
			$INSTALL $bsdpacks
			;;
		"win10")
			$INSTALL $linpacks
			;;
	esac
	echo -e "${OK}ok${NC}"
}


### [X] Cygwin   [ ] Mac   [ ] Linux   [?] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [0.1] SuSE
function installZsh() {
	if [ ! "$I_ZSH" = true ]; then
		echo -e "${TC}No zsh${NC}"
		return 0
	fi
	echo -n "Installing ZShell..."
	if [ ! -f ~/.zshrc ]; then
		local loc_rc=$BASEPATH/data/templ/zshrc.$SYSTEM
		if [ ! -f $loc_rc ]; then
			cp $BASEPATH/data/templ/zshrc.linux ~/.zshrc
		else
			cp $loc_rc ~/.zshrc
		fi
	fi
	if [ "$SHELL"=="`which zsh`" ]; then
		echo -e "${TC}Zsh already login shell${NC}"
		return 0
	fi
	echo "Setting default shell to zsh"
	chsh -s `which zsh`
	echo -e "${OK}ok${NC}"
}


### [X] Cygwin   [ ] Mac   [ ] Linux   [X] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [0.1] SuSE
function installPrograms() {
	if [ ! "$I_PROGS" = true ]; then
		echo -e "${TC}No programs${NC}"
		return 0
	fi
	echo -n "Installing programs..."
	if [ $SYSTEM == "cygwin" ]; then
		echo -e "${TC}Not necessary${NC}"
		return 0
	fi
	local packs="curl npm mc w3m links ncdu htop nmap"
	local fedorapacks="bacula-client bacula-console-bat bacula-traymonitor dosemu"
	local susepacks="tmux dosemu dos2unix ranger"
	local archpacks="mux lshw ranger dos2unix"
	local archpacks2="bacula-client vim-pathogen"
	local linpacks="mux synaptic openssh-server dos2unix bacula-client lshw vim-addon-manager vim-pathogen"
	local bsdpacks="mux bacula-client txorg xfce slim slim-themes" # xfce4
	#local ubuntu_packs=""
	$INSTALL $packs
	case $SYSTEM in
		"arch")
			$INSTALL $archpacks
			$INSTALL2 $archpacks2
			;;
		"fedora")
			$INSTALL $fedorapacks
			;;
		"suse")
			$INSTALL $susepacks
			;;
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
	echo -e "${OK}ok${NC}"
}


### [X] Cygwin   [ ] Mac   [ ] Linux   [X] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [0.1] SuSE
function installLinks() {
	if [ ! "$I_LINKS" = true ]; then
		echo -e "${TC}No links${NC}"
		return 0
	fi
	echo -n "Installing links..."
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
		if [ -f ~/.vimrc ]; then
			mv ~/.vimrc ~/.vimrc.bak
		fi
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
	if [[ ($SYSTEM == "win10") || ($SYSTEM == "cygwin") ]]; then
		return 0
	fi
	#if [ ! -L ~/launchy.ini ]; then
	#	echo "Creating launchy config"
	#	rm ~/launchy.ini
	#	ln -s $BASEPATH/etc/unix/launchy.ini ~/launchy.ini
	#fi

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
#	local autoLaunchyFn=Launchy.desktop
#	local autoLaunchyDf=$autostartDir/$autoLaunchyFn
#	if [ ! -L $autoLaunchyDf ]; then
#		ln -s $autostartSource/$autoLaunchyFn $autoLaunchyDf
#	fi
	if [ $SYSTEM == "freebsd" ]; then
		local autoFcitxFn=fcitx.desktop
		local autoFcitxDf=$autostartDir/$autoFcitxFn
		if [ ! -L $autoFcitxDf ]; then
			ln -s $autostartSource/$autoFcitxFn $autoFcitxDf
		fi
	fi
	if [ "$DEST" = "host" ]; then
		local autoOwnCloudFn=ownCloud.desktop
		local autoOwnCloudDf=$autostartDir/$autoOwnCloudFn
		if [ ! -f $autoOwnCloudDf ]; then
			echo "Creating ownCloud autostart"
			ln -s $autostartSource/$autoOwnCloudFn $autoOwnCloudDf
		fi
		#local autoTwitterFn=Twitter.desktop
		#local autoTwitterDf=$autostartDir/$autoTwitterFn
		#if [ ! -L $autoTwitterDf ]; then
		#	echo "Creating Twitter autostart"
		#	ln -s $autostartSource/$autoTwitterFn $autoTwitterDf
		#fi
		local autoMailFn=Thunderbird.desktop
		local autoMailFd=$autostartDir/$autoMailFn
		if [ ! -L $autoMailFd ]; then
			echo "Creating Thunderbird autostart"
			ln -s $autostartSource/$autoMailFn $autoMailFd
		fi
		#local autoSkypeFn=Skype.desktop
		#local autoSkypeDf=$autostartDir/$autoSkypeFn
		#if [ ! -L $autoSkypeDf ]; then
		#	echo "Creating Skype autostart"
		#	ln -s $autostartSource/$autoSkypeFn $autoSkypeDf
		#fi
	fi
	echo -e "${OK}ok${NC}"
}


### [X] Cygwin   [ ] Mac   [ ] Linux   [X] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [-] SuSE
function installXfceLinks() {
	echo -n "Installing XFCE links..."
	if [[ ($SYSTEM == "win10") || ($SYSTEM == "cygwin") ]]; then
		echo -e "${TC}Not necessary${NC}"
		return 0
	fi
	if [[ ($SYSTEM == "suse") ]]; then
		echo -e "${TC}KDE is used${NC}"
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
		if [ -f $thunarRc ]; then
			mv $thunarRc $thunarRc.bak
		fi
		ln -s $xfceSource/$thunarFn $thunarRc
	fi

	# Workspaces
	local workspaceFn=xfwm4.xml
	local workspaceRc=$channelBase/$workspaceFn
	if [ ! -L $workspaceRc ]; then
		echo "Creating workspace config"
		if [ -f $workspaceRc ]; then
			mv $workspaceRc $workspaceRc.bak
		fi
		ln -s $xfceSource/$workspaceFn $workspaceRc
	fi

	# Keyboard
	local keyboardFn=keyboards.xml
	local keyboardRc=$channelBase/$keyboardFn
	if [ ! -L $keyboardRc ]; then
		echo "Creating keyboard config"
		if [ -f $keyboardRc ]; then
			mv $keyboardRc $keyboardRc.bak
		fi
		ln -s $xfceSource/$keyboardFn $keyboardRc
	fi
	local keybLayFn=keyboard-layout.xml
	local keybLayRc=$channelBase/$keybLayFn
	if [ ! -L $keybLayRc ]; then
		echo "Creating keyboard layout config"
		if [ -f $keybLayRc ]; then
			mv $keybLayRc $keybLayRc.bak
		fi
		ln -s $xfceSource/$keybLayFn $keybLayRc
	fi

	# Notifications
	local notifyFn=xfce4-notifyd.xml
	local notifyRc=$channelBase/$notifyFn
	if [ ! -L $notifyRc ]; then
		echo "Creating notification config"
		if [ -f $notifyRc ]; then
			mv $notifyRc $notifyRc.bak
		fi
		ln -s $xfceSource/$notifyFn $notifyRc
	fi

	# Terminal
	local terminalFn=terminalrc
	local terminalRc=$xfceBase/terminal/$terminalFn
	if [ ! -L $terminalRc ]; then
		echo "Creating terminal config"
		if [ -f $terminalRc ]; then
			mv $terminalRc $terminalRc.bak
		fi
		ln -s $xfceSource/$terminalFn $terminalRc
	fi

	# Power Manager
	local powerFn=xfce4-power-manager.xml
	local powerRc=$channelBase/$powerFn
	if [ ! -L $powerRc ]; then
		echo "Creating power manager config"
		if [ -f $powerRc ]; then
			mv $powerRc $powerRc.bak
		fi
		ln -s $xfceSource/$powerFn $powerRc
	fi

	# Keyboard shortcuts
	local shortcutFn=xfce4-keyboard-shortcuts.xml
	local shortcutRc=$channelBase/$shortcutFn
	if [ ! -L $shortcutRc ]; then
		echo "Creating shortcuts config"
		if [ -f $shortcutRc ]; then
			mv $shortcutRc $shortcutRc.bak
		fi
		ln -s $xfceSource/$shortcutFn $shortcutRc
	fi

	# Panel
	local panelFn=xfce4-panel.xml
	local panelRc=$channelBase/$panelFn
	if [ ! -L $panelRc ]; then
		echo "Creating panel config"
		if [ -f $panelRc ]; then
			mv $panelRc $panelRc.bak
		fi
		ln -s $xfceSource/$panelFn $panelRc
	fi
	local panelDn=panel
	local panelDir=$xfceBase/$panelDn
	if [ ! -L $panelDir ]; then
		echo "Creating panel directory"
		if [ -f $panelDir ]; then
			mv $panelDir $panelDir.bak
		fi
		ln -s $xfceSource/$panelDn $panelDir
	fi

	# Session Manager
	local sessionFn=xfce4-session.xml
	local sessionRc=$channelBase/$sessionFn
	if [ ! -L $sessionRc ]; then
		echo "Creating session manager config"
		if [ -f $sessionRc ]; then
			mv $sessionRc $sessionRc.bak
		fi
		ln -s $xfceSource/$sessionFn $sessionRc
	fi
	echo -e "${OK}ok${NC}"
}


### [X] Cygwin   [ ] Mac   [ ] Linux   [X] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [0.1] SuSE
function installXPrograms() {
	if [ ! "$I_XPROGS" = true ]; then
		echo -e "${TC}No X11 programs${NC}"
		return 0
	fi
	if [[ ($SYSTEM == "win10") || ($SYSTEM == "cygwin") ]]; then
		return 0
	fi
	local packs="xaos thunderbird vlc wmctrl inkscape audacity gimp" #launchy devilspie corebird"
	local extPacks="bogofilter hunspell anki"
	local fedorapacks="gnome-commander chromium vim-X11 thunderbird"
	local fedoramulti="streamer1-plugins-base gstreamer1-plugins-good gstreamer1-plugins-ugly gstreamer1-plugins-bad-free gstreamer1-plugins-bad-free gstreamer1-plugins-bad-freeworld gstreamer1-plugins-bad-free-extras ffmpeg"
	local susepacks="chromium gvim retext unetbootin"
	local archpacks="doublecmd-gtk2 retext chromium mc"
	local archpacks2="gnome-commander-git file-commander-git"
	local linpacks="doublecmd-gtk vim-gtk retext chromium-browser gpgv2" # gdevilspie launchy-plugins launchy-skins "
	local linextPacks="unetbootin hunspell-de-de hunspell-ru hunspell-fr hunspell-es"
	local bsdpacks="doublecmd chromium gnupg20"
	local bsdextPacks="unetbootin owncloudclient de-hunspell ru-hunspell fr-hunspell es-hunspell"

	echo "Installing X11 programs..."
	$INSTALL $packs

	if [ ! "$DEST" = "vm" ]; then
		$INSTALL $extPacks
	fi
	case $SYSTEM in
		"arch")
			$INSTALL $archpacks
			$INSTALL $archpacks2
			;;
		"fedora")
			$INSTALL $fedorapacks
			if [ "$DEST" = "host" ]; then
				$INSTALL $fedoramulti
				$INSTALL $linextPacks
			fi
			;;
		"suse")
			$INSTALL $susepacks
			;;
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
	echo -e "${OK}ok${NC}"
}


### [X] Cygwin   [ ] Mac   [ ] Linux   [X] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [-] SuSE
function installXfcePrograms() {
	echo "Installing XFCE programs..."
	if [[ ($SYSTEM == "win10") || ($SYSTEM == "cygwin") ]]; then
		echo -e "${TC}Not necessary${NC}"
		return 0
	fi
	if [[ ($SYSTEM == "suse") ]]; then
		echo -e "${TC}KDE is used${NC}"
		return 0
	fi
	local linextPacks="xfce4-eyes-plugin"
	local bsdpacks="xfce4-xkb-plugin xfce4-weather-plugin xfce4-screenshooter-plugin xfce4-cpugraph-plugin xfce4-battery-plugin xfce4-mailwatch-plugin"

	local LOC_KWIN=`which kwin`
	if [ "$LOC_KWIN" != "" ]; then
		echo "Probably running on KDE"
	else
	case $SYSTEM in
		"arch")
			$INSTALL $bsdpacks
			;;
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
	esac
	fi
	echo -e "${OK}ok${NC}"
}

### [X] Cygwin   [ ] Mac   [ ] Linux   [X] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [0.1] SuSE
function installCompilers() {
	if [ ! "$I_COMPS" = true ]; then
		echo -e "${TC}No compilers${NC}"
		return 0
	fi
	echo -n "Installing compilers..."
	if [[ ($SYSTEM == "win10") || ($SYSTEM == "cygwin") ]]; then
		echo -e "${TC}Not necessary${NC}"
		return 0
	fi
	local packs="subversion meld cgdb gdb cmake ccache"
	local fedorapacks="mono-complete ncurses-devel cmake-gui bacula-client nodejs yarn"
	local susepacks="fsharp mono-complete cmake-gui kdevelop5 kdevelop5-pg-qt"
	local linpacks="qt5-default fsharp mono-complete nodejs yarn"
	local bsdpacks="qt5 fsharp mono nodejs yarn"
	local archpacks="qt5 mono mono-tools nodejs yarn"

	#local python="python3-pyqt5 python3-pyqt5.qtquick python3-pyqt5.qtsql python3-pyqt5.qtsvg python3-numpy python3-psycopg2"

	$INSTALL $packs
	case $SYSTEM in
		"arch")
			$INSTALL $archpacks
			if ! which fsharpc; then
				$INSTALL2 fsharp
			else
				echo "FSharp already installed"
			fi
			;;
		"fedora")
			$INSTALL $fedorapacks
			;;
		"suse")
			# $SUDO zypper ar https://download.opensuse.org/repositories/openSUSE:Factory/standard/openSUSE:Factory.repo
			# $SUDO zypper refresh
			$INSTALL $susepacks
			;;
		"ubuntu")
			$INSTALL $linpacks
			#$INSTALL $python
			;;
		"freebsd")
			$INSTALL $bsdpacks
			;;
	esac
	echo -e "${OK}ok${NC}"
}

### [X] Cygwin   [ ] Mac   [ ] Linux   [X] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [0.1] SuSE
function installTex() {
	if [ ! "$I_TEX" = true ]; then
		echo -e "${TC}No TeX${NC}"
		return 0
	fi
	if [[ ($SYSTEM == "win10") || ($SYSTEM == "cygwin") ]]; then
		echo -e "${TC}Not necessary${NC}"
		return 0
	fi
	echo -n "Installing tex..."
	local packs="texmaker lyx latex2html texstudio"
	local susepacks="latexila texlive-collection-music texlive-cyrillic"
	local linpacks="latexila texlive-music xfonts-cyrillic cjk_latex latex-cjk-japanese t1-cyrillic texlive-lang-cyrillic texlive-fonts-extra"
	local bsdpacks="latexila texlive-full font-cronyx-cyrillic font-misc-cyrillic font-screen-cyrillic xorg-fonts-cyrillic"
	local archpacks="texlive-music texlive-langcyrillic textlive-langjapanese"

	$INSTALL $packs

	case $SYSTEM in
		"ubuntu")
			$INSTALL $linpacks
			;;
		"suse")
			$INSTALL $susepacks
			;;
		"freebsd")
			$INSTALL $bsdpacks
			;;
	esac
	echo -e "${OK}ok${NC}"
}

### [X] Cygwin   [ ] Mac   [ ] Linux   [X] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [0.1] SuSE
function installGames() {
	if [ ! "$I_GAMES" = true ]; then
		echo -e "${TC}No games${NC}"
		return 0
	fi
	echo -n "Installing games..."
	if [[ ($SYSTEM == "win10") || ($SYSTEM == "cygwin") ]]; then
		echo -e "${TC}Not necessary${NC}"
		return 0
	fi
	local packs="xboard" # supertux supertuxkart
	local fedorapacks="dreamchess gnuchess"
	local archpacks="pychess"
	local susepacks="phalanx gnome-chess gnuchess lskat kiten"
	local linpacks="phalanx pychess"
	local bsdpacks="crafty brutalchess chessx pouetchess" # glchess

	$INSTALL $packs
	case $SYSTEM in
		"arch")
			$INSTALL $archpacks
			;;
		"ubuntu")
			$INSTALL $linpacks
			;;
		"suse")
			$INSTALL $susepacks
			;;
		"freebsd")
			$INSTALL $bsdpacks
			;;
	esac
	echo -e "${OK}ok${NC}"
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


### [X] Cygwin   [ ] Mac   [ ] Linux   [X] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [0.1] SuSE
function cloneGithub() {
	if [ ! "$I_GH" = true ]; then
		echo -e "${TC}No github${NC}"
		return 0
	fi
	echo -n "Cloning github..."
	local srcpath=~/work/github
	if [ $SYSTEM == "win10" ]; then
		srcpath=/mnt/c/work/github
	fi
	if [ ! -d "$srcpath" ]; then
		echo -e "${TC}Error: $srcpath does not exist, Creating ${NC}"
		mkdir -p $srcpath
	fi
	pushd .
	mkdir -p $srcpath
	cd $srcpath
	if [ ! -d Poseidon ]; then
		echo "Cloning Poseidon"
		git clone git@github.com:slesa/Poseidon
		cd Poseidon && git flow init -d && git checkout develop && cd ..
	fi
	if [ ! -d gui.cs ]; then
		echo "Cloning gui.cs"
		git clone git@github.com:slesa/gui.cs
		cd gui.cs && git flow init -d && git checkout develop && cd ..
	fi
	if [ ! -d sqlitestudio ]; then
		echo "Cloning sqlitestudio"
		git clone git@github.com:slesa/sqlitestudio
		cd sqlitestudio && git flow init -d && git checkout develop && cd ..
	fi
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
	#if [ ! -d fable-react_native-demo ]; then
	#	echo "Cloning fable-react_native-demo"
	#	git clone git@github.com:slesa/fable-react_native-demo
	#	cd fable-react_native-demo && git flow init -d && cd ..
	#fi
	if [ ! -d fable-elmish ]; then
		echo "Cloning fable-elmish"
		git clone git@github.com:slesa/fable-elmish
	fi
	#if [ ! -d GammaRay ]; then
	#	git clone https://github.com/KDAB/GammaRay
		#cd GammaRay && mkdir build && cd build && cmake .. && make && cd ../..
	#fi
	popd
}

### [X] Cygwin   [ ] Mac   [ ] Linux   [X] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [0.1] SuSE
function cloneGitlab() {
	if [ ! "$I_GL" = true ]; then
		echo -e "${TC}No gitlab${NC}"
		return 0
	fi
	echo -n "Cloning gitlab..."
	pushd .
	mkdir -p ~/work/gitlab
	cd ~/work/gitlab
	if [ ! -d waiterwatch ]; then
		echo "Cloning waiterwatch"
		git clone git@gitlab.com:slesa/waiterwatch
		cd waiterwatch && git flow init -d && git checkout develop && cd ..
	fi
	if [ ! -d aikidoka ]; then
		echo "Cloning aikidoka"
		git clone git@gitlab.com:slesa/aikidoka
		cd aikidoka && git flow init -d && git checkout develop && cd ..
	fi
	if [ ! -d monty ]; then
		echo "Cloning monty"
		git clone git@gitlab.com:slesa/monty
		# cd monty && git flow init -d && git checkout develop && cd ..
	fi
	popd
}

### [X] Cygwin   [ ] Mac   [ ] Linux   [X] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [-] SuSE
function installLogin() {
	if [ ! "$I_LOGIN" = true ]; then
		echo -e "${TC}No login wallpapers${NC}"
		return 0
	fi
	echo -n "Installing login wallpapers..."
	case $SYSTEM in
		"arch"|"ubuntu")
			if [ -f /usr/share/backgrounds/StarTrekLogo1920x1080.jpg ]; then
				echo -e "${TC}Login logo already installed${NC}"
				return 0
			fi
			sudo cp $BASEPATH/data/img/StarTrekLogo1920x1080.jpg /usr/share/backgrounds
			sudo chmod +r /usr/share/backgrounds/StarTrekLogo1920x1080.jpg
			sudo sed -i '/background=/c\background=/usr/share/backgrounds/StarTrekLogo1920x1080.jpg' /etc/lightdm/lightdm-gtk-greeter.conf
			#sudo sed -i '/#background=/c\background=/usr/share/backgrounds/StarTrekLogo1920x1080.jpg' /etc/lightdm/lightdm-gtk-greeter.conf
			;;
		"suse"|"fedora")
			if [ -f /usr/share/wallpapers/StarTrekLogo1920x1080.jpg ]; then
				echo -e "${TC}Login logo already installed${NC}"
				return 0
			fi
			if [ -f /etc/lightdm/lightdm-gtk-greeter.conf ]; then
				sudo cp $BASEPATH/data/img/StarTrekLogo1920x1080.jpg /usr/share/wallpapers/
				sudo chmod +r /usr/share/wallpapers/StarTrekLogo1920x1080.jpg
				sudo sed -i '/background=/c\background=/usr/share/wallpapers/StarTrekLogo1920x1080.jpg' /etc/lightdm/lightdm-gtk-greeter.conf
				#sudo sed -i '/#background=/c\background=/usr/share/backgrounds/StarTrekLogo1920x1080.jpg' /etc/lightdm/lightdm-gtk-greeter.conf
			fi
			;;
		"freebsd")
			if [ -f /usr/local/share/backgrounds/StarTrekLogo1920x1080.jpg ]; then
				echo -e "${TC}Login logo already installed${NC}"
				return 0
			fi
			sudo cp $BASEPATH/data/img/StarTrekLogo1920x1080.jpg /usr/local/share/PCDM/themes/trueos
			sudo chmod +r /usr/local/share/PCDM/themes/trueos/StarTrekLogo1920x1080.jpg
			sudo sed -i -e "s/BACKGROUND_IMAGE=.*/BACKGROUND_IMAGE=StarTrekLogo1920x1080.jpg/g" /usr/local/share/PCDM/themes/trueos/trueos.theme
			;;
		"cygwin"|"win10")
			echo -e "${TC}Not necessary${NC}"
			return 0
			;;
	esac
	echo -e "${Ok}Ok${NC}"
}


### ----------------------------------------------------------------------------------------------
### External installers
### ----------------------------------------------------------------------------------------------

function installQt() {
	if [ "$NO_QT" = true ]; then
		echo "Ignore Qt"
		return 0
	fi
	if [ -d ~/work/Qt ] || [ -d ~/work/qt ]; then
		echo "qt5 already installed"
		return 0
	fi
	echo "Installing qt5"
	pushd . && cd ~/Downloads
	if [ ! -f qt-unified-linux-x64-online.run ]; then
		wget https://download.qt.io/official_releases/online_installers/qt-unified-linux-x64-online.run
	fi
	chmod +x qt-unified-linux-x64-online.run
	./qt-unified-linux-x64-online.run &
	popd
}

function installRider() {
	if [ "$NO_RIDER" = true ]; then
		echo "Ignore Rider"
		return 0
	fi
	if [ -d ~/bin/Jetbrains.Rider ]; then
		echo "Rider already installed"
		return 0
	fi
	pushd . && cd ~/Downloads
	if [ ! -f JetBrains.Rider-2019.2.3.tar.gz ]; then
		wget https://download.jetbrains.com/rider/JetBrains.Rider-2019.2.3.tar.gz
	fi
	cd ~/bin
	tar xvzf ~/Downloads/JetBrains.Rider-2019.2.3.tar.gz
	mv JetBrains\ Rider* JetBrains.Rider
	popd
}

function installPyCharm() {
	if [ "$NO_CHARM" = true ]; then
		echo "Ignore PyCharm"
		return 0
	fi
	if [ -d ~/bin/Jetbrains.PyCharm ]; then
		echo "PyCharm already installed"
		return 0
	fi
	pushd . && cd ~/Downloads
	if [ ! -f pycharm-community-2019.2.4.tar.gz ]; then
		wget https://download.jetbrains.com/python/pycharm-community-2019.2.4.tar.gz
	fi
	cd ~/bin
	tar xvzf ~/Downloads/pycharm-community-2019.2.4.tar.gz
	mv pycharm-community* Jetbrains.PyCharm
	popd
}

function installSkype() {
	if [ "$NO_SKYPE" = true ]; then
		echo "Ignore Skype"
		return 0
	fi
	if [ -d /usr/bin/skype ]; then
		echo "Skype already installed"
		return 0
	fi
	pushd . && cd ~/Downloads
	if [ ! -f skypeforlinux-64.rpm ]; then
		wget https://go.skype.com/skype.download/skypeforlinux-64.rpm ]
	fi
	sudo rpm -i skypeforlinux-64.rpm
	popd
}

function installGitKraken() {
	if [ -f /usr/share/gitkraken/gitkraken ]; then
		echo "gitkraken already installed"
		return 0
	fi
	echo "Installing Gitkraken..."
	pushd . && cd ~/Downloads
	if [ ! -f gitkraken-amd64.rpm ]; then
		wget https://release.gitkraken.com/linux/gitkraken-amd64.rpm
	fi
	rpm -i gitkraken-amd64.rpm
	popd
}

### [X] Cygwin   [ ] Mac   [ ] Linux   [X] FreeBSD   [ ] LinuxOnWin  [X] Manjaro  [0.1] SuSE
function installExternals() {
	if [ ! "$I_EXT" = true ]; then
		echo -e "${TC}No external apllications${NC}"
		return 0
	fi
	echo "Installing external applications..."
	case $SYSTEM in
		"suse")
			# Keybase
			$INSTALL keybase-client
			# Visual Studio Code
			$SUDO zypper addrepo https://download.opensuse.org/repositories/devel:tools:scm/openSUSE_Tumbleweed/devel:tools:scm.repo
			$SUDO zypper refresh
			$INSTALL code
			# Gitkraken
			#wget https://www.gitkraken.com/download/linux-rpm
			# Sublime Text
			$SUDO rpm -v --import https://download.sublimetext.com/sublimehq-rpm-pub.gpg
			$SUDO zypper addrepo -g -f https://download.sublimetext.com/rpm/stable/x86_64/sublime-text.repo
			$INSTALL install sublime-text
			# Externals
			installQt
			installRider
			installPyCharm
			installSkype
			installGitKraken
			;;
		"arch")
			$INSTALL keybase
			if ! which code; then
				$INSTALL2 visual-studio-code-bin 
			else
				echo "Visual Studio Code already installed"
			fi
			if ! which gitkraken; then
				$INSTALL2 gitkraken 
			else
				echo "GitKraken already installed"
			fi
			if ! which sky; then
				sky
			else
				echo "Sky(pe) already installed"
			fi
			;;
		"fedora")
			# Visual Studio Code
			if ! which code; then
				echo "Installing VS Code"
				sudo cp etc/fedora/vscode.repo /etc/yum.repos.d/
				sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
				sudo yum check-update
				$INSTALL code
			else    
				echo "VS Code already installed"
			fi
			if [ -f /etc/yum.repo.d/microsoft-prod.repo ]; then
				echo -e "${TC}Microsoft repo already present"
			else
				wget -q https://packages.microsoft.com/config/fedora/27/prod.repo
				sudo mv prod.repo /etc/yum.repos.d/microsoft-prod.repo
				sudo chown root:root /etc/yum.repos.d/microsoft-prod.repo
				sudo yum check-update
				$INSTALL dotnet-sdk-2.2
			fi
			# Keybase
			if ! which keybase; then
				echo "Installing keybase"
				sudo dnf install -y https://prerelease.keybase.io/keybase_amd64.rpm
				run_keybase
			else
				echo "Keybase already installed"
			fi
			installQt
			installRider
			installPyCharm
			;;
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
			#if ! which subl; then
			#	echo "Installing sublime text"
			#	wget https://download.sublimetext.com/sublime-text_build-3114_amd64.deb
			#	sudo dpkg -i sublime-text_build-3126_amd64.deb
			#else
			#	echo "Sublime already installed"
			#fi

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

			installQt
			installRider
			installPyCharm
			;;
		"freebsd")
			$INSTALL keybase linux-sublime3 qt5
			;;
		"cygwin")
			;;
	esac
}


echo -e "${HEAD}[=== Configuring system ===]${NC}"
getSystem
echo -e "System is ${SYSTEM}"

readArguments $@
if [ ! "$I_ARGS" == "true" ]; then
	printHelp
	exit 1
fi
if [ "$SYSTEM" == "unknown" ]; then
	echo "No valid system found"
	exit 1
fi

ensureRoot
installCore
installOwnCube
createSshKey
installDotFiles
installFonts
installBasics
installZsh
installPrograms
installLinks
installXfceLinks # no arg
installXPrograms
installXfcePrograms # no arg
installCompilers
installLogin
installTex
installGames
##installTwitter
cloneGithub
cloneGitlab
installExternals
echo "Done"
