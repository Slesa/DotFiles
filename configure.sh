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

#function installOwnCube() {
#    sudo sh -c "echo 'deb http://download.opensuse.org/repositories/isv:/ownCloud:/desktop/Ubuntu_16.10/ /' > /etc/apt/sources.list.d/owncloud-client.list"
#    sudo apt-get update
#    sudo apt-get install owncloud-client
#}


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

function installPrograms() {
    local packs="curl npm mc w3m links ncdu htop nmap vim bacula-client"
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
    #if [ ! -d ~/.config/xfce4.orig ]; then
    #    echo "Creating xfce configs"
    #    mv ~/.config/xfce4 ~/.config/xfce4.orig
    #    cp -r $BASEPATH/etc/unix/xfce4 ~/.config/xfce4
    #fi

    echo "Creating autostarts"
    if [ ! -d ~/.config/autostart ]; then
        mkdir ~/.config/autostart
    fi

#    if [ ! -L ~/.config/autostart/devilspie.desktop ]; then
#        ln -s $BASEPATH/etc/unix/autostart/devilspie.desktop ~/.config/autostart/devilspie.desktop
#    fi
#    if [ ! -L ~/.config/autostart/Pidgin.desktop ]; then
#        ln -s $BASEPATH/etc/unix/autostart/Pidgin.desktop ~/.config/autostart/Pidgin.desktop
#    fi
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
        if [ ! -L ~/.config/autostart/Skype.desktop ]; then
            ln -s $BASEPATH/etc/unix/autostart/Skype.desktop ~/.config/autostart/Skype.desktop
        fi
    fi
}


function installXPrograms() {
    local packs="launchy thunderbird devilspie wmctrl inkscape audacity vlc gimp"
    local extPacks="bogofilter hunspelli anki"
    local linpacks="launchy-plugins launchy-skins doublecmd-gtk vim-gtk gdevilspie retext chromium-browser"
    local linextPacks="owncloud-client hunspell-de-de hunspell-ru hunspell-fr hunspell-es"
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

function installXfcePrograms() {
    local linextPacks="xfce4-eyes-plugin"
    local bsdpacks="xfce4-xkb-plugin xfce4-weather-plugin xfce-screenshooter-plugin xfce-cpugraph-plugin"

    local LOC_KWIN=`which kwin`
    if [ $LOC_KWIN != "" ]; then
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
    local packs="subversion meld cgdb gdb cmake"
    local linpacks="qt5-default fsharp mono-complete"
    local bsdpacks="qt5"

    local python="python3-pyqt5 python3-pyqt5.qtquick python3-pyqt5.qtsql python3-pyqt5.qtsvg python3-numpy python3-psycopg2"

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
    echo "Installing external applications..."
    case $SYSTEM in
        "ubuntu")
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
            # Visual Studio Code
            if ! which code; then
                echo "Installing VS Code"
                wget https://go.microsoft.com/fwlink/?LinkID=760868
                sudo dpkg -i `find . -name code*_amd64.deb`
            else    
                echo "VS Code already installed"
            fi

            if [ ! -d ~/work/qt ]; then
                echo "Installing qt5"
                wget http://download.qt.io/official_releases/online_installers/qt-unified-linux-x64-online.run
                chmod +x qt-unified-linux-x64-online.run
                ./qt-unified-linux-x64-online.run
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
    pushd .
    mkdir -p ~/work/github
    cd ~/work/github
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
    echo "Please mention either host or slave"
    exit 1
fi
if [ "$SYSTEM" == "unknown" ]; then
    echo "No valid system found"
    exit 1
fi

getSystem
ensureRoot
installPrereqs
#installOwnCube
createSshKey
installDotFiles
installFonts
installBasics
installZsh
installPrograms
installLinks
installXPrograms
installXfcePrograms
installCompilers
installTwitter
installGames
installTex
installExternals
installLogin
cloneGithub
cloneGitlab
echo "Done"
