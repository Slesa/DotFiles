# [01] Fedora       [01] FreeBSD     [01] Arch/Manjaro   [01] SuSE Tumbleweed
# [02] Ubuntu WSL   [01] Cygwin      [01] MX             [01] Mageia
from setup.osplatform import Systems, Subsys
from setup.console import output
from setup.helpers import flag_is_set, install
import subprocess

def install_core(installprog, targetsys, subsys, options):
    output('Collect core............: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.core, options.nocore):
        output('<yellow>pass<nc>')
        return

    if subsys == Subsys.Windows:
        if targetsys == Systems.Ubuntu:
            subprocess.check_call(['sudo', 'add-apt-repository', 'ppa:neovim-ppa/unstable'])
            subprocess.check_call(['sudo', 'apt-get', 'update'])

    if targetsys == Systems.Fedora or targetsys == Systems.Mageia:
        import os
        version = os.popen('rpm -E %fedora').read()[:-1]
        output(f'Fedora {version}')
        subprocess.check_call(['sudo', 'dnf', 'install', '-y', f'https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-{version}.noarch.rpm'])

    packages = ['zsh', 'neovim']
    if targetsys != Systems.Debian:
        packages += ['neofetch']
    if subsys == Subsys.Origin:  # Not needed on Win Subsys
        packages += ['git']
        if targetsys == Systems.FreeBSD:
            packages += ['firefox-esr']
        elif targetsys != Systems.Raspbian:
            packages += ['firefox']
    if targetsys == Systems.SunOS:
        packages += ['links', 'wget', 'rsync']
    if targetsys == Systems.FreeBSD or targetsys == Systems.NetBSD or targetsys == Systems.OpenBSD:
        packages += ['pidof', 'links', 'wget', 'rsync', 'bsdstats', 'neovim']
        if targetsys == Systems.FreeBSD:
            packages += ['linux_base-c7', 'portmaster', 'portshaker', 'poudriere-devel']
    else:
        if targetsys != Systems.Arch:
            packages += ['vim']
        if targetsys != Systems.Raspbian:
            packages += ['xsel']
    install(installprog, packages)
    output('<green>Ok<nc>')



class Installer:
    def __init__(self, targetsys, subsys, options):
        self.targetsys = targetsys
        self.subsys = subsys
        self.options =  options
        self.pkg_basics = self.create_basic_packages()
        self.pkg_programs = self.create_program_packages()
        self.pkg_xprograms = self.create_xprogram_packages()
        self.pkg_compiler = self.create_compiler_packages()
        self.pkg_xfce = self.create_xfce_packages()
        self.pkg_i3wm = self.create_i3wm_packages()
        self.pkg_tex = self.create_tex_packages()
        self.pkg_games = self.create_games_packages()
        self.pkg_nextcloud = self.create_nextcloud_packages()

    # ['git-flow']
    def create_basic_packages(self):
        pkgs = {
            Systems.Unknown:
                ['zsh'],
            Systems.Arch:
                ['synergy', 'fortune-mod', 'zsh-lovers', 'taskwarrior'],
            Systems.SunOS:
                ['synergy', 'rdesktop'],
            Systems.Fedora:
                ['fortune-mod', 'keybase', 'zsh-lovers', 'rdesktop', 'gcc-c++', 'synergy', 'task', 'fastfetch', 'cheat'],
            Systems.OpenBSD:
                ['inotify-tools', 'pstree', 'synergy', 'ssh-copy-id', 'keybase', 'zsh-syntax-lightning', 'taskwarrior', 'pkglocatedb'],
            Systems.NetBSD:
                ['pstree', 'synergy', 'fortunes-de', 'taskwarrior'],
            Systems.FreeBSD:
                ['inotify-tools', 'pstree', 'synergy', 'gitflow', 'keybase', 'fortune-mod-bofh', 'taskwarrior', 'cheat'],
            Systems.Mageia:
                ['synergy', 'gitflow', 'fortune-mod', 'fortune-murphy'],
            Systems.MxLinux:
                ['git-flow', 'fortunes', 'fortunes-de'],
            Systems.Ubuntu:
                ['git-flow', 'fortunes', 'fortunes-de', 'taskwarrior'],
            Systems.Redhat:
                ['fortune-mod', 'rdesktop', 'gcc-c++', 'synergy'],
            Systems.SuSE:
                ['fortune', 'synergy', 'qsynergy', 'rdesktop', 'gcc-c++', 'gcc'],
            Systems.Raspbian:
                ['fortune-mod'],
            Systems.Debian:    
                ['fastfetch', 'taskwarrior', 'fortune-mod', 'fortunes', 'fortunes-de']
        }
        if self.subsys == Subsys.Origin:
            pkgs[Systems.Ubuntu] += ['hfsplus', 'synergy', 'rdesktop']
        return pkgs

    def getpkgs_basics(self):
        output('Collect basics..........: ', False)
        output(str(self.targetsys))
        if self.targetsys == Systems.Cygwin:
            output('<tc>not necessary<nc>')
            return []
        if not flag_is_set(self.options, self.options.basics, self.options.nobasics):
            output('<yellow>pass<nc>')
            return []
        result =  self.pkg_basics[Systems.Unknown] + self.pkg_basics[self.targetsys]
        output('<green>Ok<nc>')
        return result

    def create_program_packages(self):
        pkgs = {
            Systems.Unknown:
                ['curl', 'ncdu', 'htop', 'nmap'],
            Systems.Arch:
                ['mc', 'npm', 'links', 'w3m', 'postgresql', 'byobu', 'tmux', 'ranger', 'dos2unix', 'lshw'],
            Systems.SunOS:
                ['links', 'w3m', 'postgresql', 'tmux'],
            Systems.Fedora:
                ['mc', 'npm', 'links', 'w3m', 'postgresql', 'byobu', 'postgresql-server', 'postgresql-contrib', 'tmux'],
            Systems.OpenBSD:
                ['mc', 'postgresql-server', 'postgresql-client'],
            Systems.NetBSD:
                ['mc', 'postgresql16-server', 'postgresql16-client', 'tmux', 'hs-pandoc', 'byobu'],
            Systems.FreeBSD:
                # [xfce slim slim-themes]
                ['mc', 'npm', 'links', 'w3m', 'postgresql16-server', 'postgresql16-client', 'tmux', 'hs-pandoc', 'byobu'],
            Systems.Mageia:
                ['mc', 'npm', 'links', 'w3m', 'postgresql16', 'postgresql16-server', 'tmux', 'ranger', 'dos2unix', 'openssh-server', 'byobu'],
            Systems.MxLinux:
                ['mc', 'npm', 'links', 'w3m', 'postgresql-15', 'tmux', 'ranger', 'dos2unix', 'openssh-server', 'vim-addon-manager',
                 'vim-pathogen', 'byobu'],
            Systems.Ubuntu:
                ['mc', 'npm', 'links', 'w3m', 'postgresql', 'byobu', 'tmux', 'ranger', 'dos2unix', 'vim-addon-manager', 'vim-pathogen'],
            Systems.Redhat:
                ['mc', 'npm', 'links', 'w3m', 'postgresql-server', 'postgresql-contrib', 'tmux'],
            Systems.SuSE:
                ['mc', 'npm', 'links', 'w3m', 'postgresql', 'byobu', 'tmux', 'ranger', 'dos2unix', 'dosemu'],
            Systems.Raspbian:
                [],
            Systems.Debian:
                ['postgresql', 'byobu', 'tmux', 'ranger', 'dos2unix']
        }
        if self.subsys == Subsys.Origin:
            pkgs[Systems.Ubuntu] += ['synaptic', 'openssh-server', 'lshw']
        return pkgs

    def getpkgs_programs(self):
        # Ubuntu: tmuxinator, tmux-plugin-manager ranger
        output('Collect programs........: ', False)
        if self.targetsys == Systems.Cygwin:
            output('<tc>not necessary<nc>')
            return []
        if not flag_is_set(self.options, self.options.programs, self.options.noprograms):
            output('<yellow>pass<nc>')
            return []
        result =  self.pkg_programs[Systems.Unknown] + self.pkg_programs[self.targetsys]
        output('<green>Ok<nc>')
        return result

    def create_xprogram_packages(self):
        pkgs = {
            Systems.Unknown:
                ['thunderbird', 'inkscape', 'gimp', 'bogofilter', 'hunspell', 'hexchat'],
            Systems.Arch:
                ['anthy', 'audacity', 'ibus-anthy', 'xaos', 'retext', 'chromium', 'gvim', 'doublecmd-gtk2',
                 'brave-browser', 'code', 'keybase', 'keybase-gui', 'xpdf',
                 'lollypop', 'easytag', 'asunder', 'elisa', 'strawberry',
                 'qemu', 'virt-manager'],
            Systems.SunOS:
                ['anthy', 'gvim', 'gnome-commander', 'hexchat',
                 'rhythmbox', 'totem',
                 'qemu', 'virt-manager'],
            Systems.Fedora:
                ['anthy', 'audacity', 'ibus-anthy', 'xaos', 'gnome-commander', 'chromium', 'vim-X11', 'gstreamer1-plugins-good',
                 'gstreamer1-plugins-bad-free', 'gstreamer1-plugins-bad-free-extras', 'unetbootin', #'anki',
                 'hunspell-de', 'hunspell-ru', 'hunspell-fr', 'hunspell-es',
                 'kitty', 'worker', 'ghostwriter',
                 'qemu', 'virt-manager'],
            Systems.OpenBSD:
                ['anthy', 'ibus-anthy', 'xaos','vlc', 'gnupg', 'chromium', 'totem',
                 'vlc', 'gnupg', 'tor-browser', 'audacity', 'anki',
                 'xpdf', 'kitty', 'xfe', 'rhythmbox', 'noto-nerd-fonts', 'terminus-nerd-fonts', 'ubuntu-nerd-fonts', 'ubuntumono-nerd-fonts',
                 'easytag', 'worker',
                 'qemu'
                 ],
            Systems.NetBSD:
                ['anthy', 'ibus-anthy', 'xaos','vlc', 'gnupg', 
                 'vlc', 'gnupg', 'hunspell-de', 'hunspell-ru_RU', 'hunspell-fr_FR', 'hunspell-es_ES',
                 'xpdf', 'kitty', 'lazygit', 'xfe', 'nerd-fonts',  
                 'exaile', 'easytag', 'asunder', 'strawberry', 'worker',
                 'qemu'
                 ],
            Systems.FreeBSD:
                ['ja-anthy', 'xaos','vlc', 'gnupg', 'anki',
                 'chromium', 'vlc', 'gnupg', 'unetbootin', 'de-hunspell', 'ru-hunspell', 'fr-hunspell', 'es-hunspell',
                 'ja-font-kochi', 'ja-ibus-anthy', 
                 'ghostwriter', 'xorg', 'xpdf', 'kitty', 'lazygit', 'xfe', 'nerd-fonts', 'neovim-gtk',
                 'lollypop', 'exaile', 'easytag', 
                 'iridium-browser', 'strawberry', 'rhythmbox', 'worker',
                 'qemu', 'virt-manager', 'cpu-x', 'vscode' 
                 ],
            Systems.Mageia:
                ['anthy', 'audacity', 'ibus-anthy', 'xaos', 'chromium-browser', 'vim-X11', 'vlc', 'gnome-commander', 'unetbootin', 'rhythmbox', 'anki',
                 'hunspell-de', 'hunspell-es', 'hunspell-ru', 'hunspell-fr',
                 'fonts-ttf-japanese', 'fonts-ttf-japanese-extra', 'google-noto-sans-cjk-jp-fonts', 'google-noto-sans-jp-fonts', 'google-noto-serif-jp-fonts', 'google-noto-serif-cjk-jp-fonts'
                 ],
            Systems.MxLinux:
                ['anthy', 'audacity', 'ibus-anthy', 'xaos', 'retext', 'vlc', 'tuxcmd', 'gpgv2', 'hunspell-ru', 'hunspell-fr', 'hunspell-es',
                 'hunspell-de-de', 'chromium'],
            Systems.Ubuntu:
                ['anthy', 'audacity', 'ibus-anthy', 'xaos', 'vim-gtk', 'retext', 'vlc', 'tuxcmd', 'gpgv2', 'hunspell-ru', 'hunspell-fr', 'hunspell-es', 'anki',
                 'hunspell-de', 'chromium-browser'],
            Systems.Redhat:
                ['anthy', 'audacity', 'ibus-anthy', 'chromium', 'vim-X11', 'gstreamer1-plugins-good', 'gstreamer1-plugins-bad-free',
                 'hunspell-de', 'hunspell-ru', 'hunspell-fr', 'hunspell-es'],
            Systems.SuSE:
                ['anthy', 'audacity', 'ibus-anthy', 'xaos', 'chromium', 'gvim', 'vlc', 'gnome-commander', 'retext', 'unetbootin', 'rhythmbox'], #, 'anki']
        }
        return pkgs

    def getpkgs_xprograms(self):
        # Ubuntu: xaos, guake
        output('Collect X programs......: ', False)
        if self.targetsys == Systems.Cygwin or self.subsys == Subsys.Windows:
            output('<tc>not necessary<nc>')
            return []
        if not flag_is_set(self.options, self.options.xprograms, self.options.noxprograms):
            output('<yellow>pass<nc>')
            return []
        result = self.pkg_xprograms[Systems.Unknown] + self.pkg_xprograms[self.targetsys]
        if self.targetsys == Systems.SunOS:
            result.remove('bogofilter')
            result.remove('wmctrl')
            result.remove('asunder')
        output('<green>Ok<nc>')
        return result

    def create_compiler_packages(self):
        pkgs = {
            Systems.Unknown:
                ['meld', 'gdb', 'cmake', 'ccache'],
            Systems.Arch:
                ['cgdb', 'jdk-openjdk', 'nodejs', 'yarn', 'docker-compose',
                 'dotnet-runtime', 'dotnet-sdk', 'dotnet-targeting-pack', 'aspnet-runtime', 'aspnet-targeting-pack',
                 'dotnet-runtime-7.0', 'dotnet-sdk-7.0', 'dotnet-targeting-pack-7.0', 'aspnet-runtime-7.0', 'aspnet-targeting-pack-7.0'],
            Systems.SunOS:
                ['build-essential', 'gcc-13', 'qt6', 'qtcreator', 'nodejs-20', 'rustc', 'cmake', 'codeblocks'],
            Systems.Fedora:
                ['cgdb', 'ncurses-devel', 'cmake-gui', 'nodejs', 'mesa-libGL', 'mesa-libGL-devel', 
                 'rust-cargo-devel', 'dotnet', 'qt-creator', 'elixir', 'elixir-doc', 'erlang',
                 'dotnet-runtime-7.0', 'dotnet-sdk-7.0', 'dotnet-targeting-pack-7.0', 'dotnet-apphost-pack-7.0', 'dotnet-templates-7.0',
                 'dotnet-runtime-8.0', 'dotnet-sdk-8.0', 'dotnet-targeting-pack-8.0', 'dotnet-apphost-pack-8.0', 'dotnet-templates-8.0',
                 'PackageKit-Qt6-devel', 'qt6-qtbase-devel', 'qt6-qtcharts-devel', 'qt6-qtconnectivity-devel', 'qt6-qtdeclarative-devel',
                 'qt6-qtgraphs-devel', 'qt6-qtgrpc-devel', 'qt6-qthttpserver-devel', 'qt6-qtlanguageserver-devel', 'qt6-qtlocation-devel',
                 'qt6-qtlottie-devel', 'qt6-qtmqtt-devel', 'qt6-qtmultimedia-devel', 'qt6-qtnetworkauth-devel', 'qt6-qtopcua-devel',
                 'qt6-qtpdf-devel', 'qt6-qtpositioning-devel', 'qt6-qtgraphs-devel', 'qt6-qtremoteobjects-devel', 'qt6-qtscxml-devel',
                 'qt6-qtsensors-devel', 'qt6-qtserialbus-devel', 'qt6-qtspeech-devel', 'qt6-qtsvg-devel', 'qt6-qtvirtualkeyboard-devel',
                 'qt6-qtwebchannel-devel', 'qt6-qtwebsockets-devel', 'qt6-qtwebview-devel', 'qtsingleapplication-qt6-devel', 
                 'kdsoap-ws-discovery-client-devel',
                 ],
            Systems.OpenBSD:
                ['qt-creator', 'node', 'yarn', 'jdk17', 'rust',  
                 'elixir', 'erlang'
                ],
            Systems.NetBSD:
                ['qtcreator', 'nodejs', 'yarn', 'openjdk17', 'rust', 'docker', 
                 'elixir', 'erlang'
                 #'qt6', 'qt6-qtbase', 'qt6-qtcharts', 'qt6-qtdeclarative', 'qt6-qthttpserver', 'qt6-qtimageformats',
                 #'qt6-qtlanguageserver', 'qt6-qtlocation', 'qt6-qtmultimedia', 'qt6-qtnetworkauth', 'qt6-qtpositioning', 'qt6-qtremoteobjects', 
                 #'qt6-qtscxml', 'qt6-qtserialport', 'qt6-qtspeech', 'qt6-qtsvg', 'qt6-qttools', 'qt6-qttranslations', 
                 #'qt6-qtvirtualkeyboard', 'qt6-qtwebchannel', 'qt6-qtwebsockets', 'qt6ct'
                ],
            Systems.FreeBSD:
                # ['fsharp', 'mono', ]
                #['cgdb', 'qtcreator', 'node20', 'npm', 'yarn', 'openjdk17'],
                ['qtcreator', 'node20', 'npm', 'yarn', 'openjdk17', 'rust', 'docker', 'docker-machine',
                 'qt6', 'qt6-base', 'qt6-charts', 'qt6-declarative', 'qt6-doc', 'qt6-examples', 'qt6-httpserver', 'qt6-imageformats',
                 'qt6-languageserver', 'qt6-location', 'qt6-multimedia', 'qt6-networkauth', 'qt6-positioning', 'qt6-remoteobjects', 
                 'qt6-scxml', 'qt6-serialbus', 'qt6-serialport', 'qt6-speech', 'qt6-svg', 'qt6-tools', 'qt6-translations', 
                 'qt6-virtualkeyboard', 'qt6-webchannel', 'qt6-webengine', 'qt6-websockets', 'qt6-webview', 'qt6ct'
                ],
            Systems.Mageia:
                ['cgdb', 'cmake-qtgui', 'nodejs', 'lib64mesagl-devel'],
            Systems.MxLinux:
                ['cgdb', 'python3-venv', 'cmake-qt-gui', 'yarnpkg',
                 'libgl1-mesa-dev', 'libglu1-mesa-dev'],
            Systems.Ubuntu:
                # [ 'fsharp', ]
                ['cgdb', 'nodejs', 'yarn', 'rust', 'rust-cargo-devel'],
            Systems.Redhat:
                ['cgdb', 'ncurses-devel', 'cmake-gui', 'nodejs', 'mesa-libGL', 'mesa-libGL-devel'
                    , 'dotnet', 'dotnet-sdk-6.0', 'dotnet-templates-6.0'],
            Systems.SuSE:
                # ['mono-complete','fsharp',]
                ['cgdb', 'nodejs19', 'yarn', 'cmake-gui', 'rust', 'rust-cargo-devel', 'libboost-all-dev'],
            Systems.Debian:
                # curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
                ['cgdb', 'nodejs', 'cmake-gui', 'qtcreator', 'elixir', 'libboost-all-dev', 'gettext', 'pkg-config', 'protobuf-compiler',
                 'qt6-base-dev', 'qt6-base-dev-tools', 'qt6-base-doc', 'qt6-base-examples',
                ]
        }
        if self.targetsys != Systems.Cygwin and self.subsys != Subsys.Windows:
            pkgs += ['docker']
        return pkgs

    def getpkgs_compiler(self):
        output('Collect compiler........: ', False)
        if self.targetsys == Systems.Cygwin:
            output('<tc>not necessary<nc>')
            return []
        if not flag_is_set(self.options, self.options.compiler, self.options.nocompiler):
            output('<yellow>pass<nc>')
            return []
        result = self.pkg_compiler[Systems.Unknown] + self.pkg_compiler[self.targetsys]
        output('<green>Ok<nc>')
        return result

    def create_xfce_packages(self):
        pkgs = {
            Systems.Unknown:
                [],
            Systems.Arch:
                ['xfwm4-themes', 'xfce4-xkb-plugin', 'xfce4-weather-plugin', 'xfce4-cpugraph-plugin',
                 'xfce4-battery-plugin', 'xfce4-wavelan-plugin', 'xfce4-clipman-plugin', 'xfce4-netload-plugin',
                 'xfce4-pulseaudio-plugin'],
            Systems.SunOS:
                [],
            Systems.Fedora:
                ['xfwm4-themes', 'xfce4-eyes-plugin'],
            Systems.OpenBSD:
                ['xfwm4-themes', 'xfce4-xkb', 'xfce4-weather', 'xfce4-cpugraph',
                 'xfce4-battery', 'xfce4-wavelan', 'xfce4-clipman', 'xfce4-netload',
                 'xfce4-screenshooter'],
            Systems.NetBSD:
                ['xfce4-wm-themes', 'xfce4-xkb-plugin', 'xfce4-weather-plugin', 'xfce4-cpugraph-plugin',
                 'xfce4-battery-plugin', 'xfce4-wavelan-plugin', 'xfce4-clipman-plugin', 'xfce4-netload-plugin',
                 'xfce4-screenshooter'],
            Systems.FreeBSD:
                ['xfce4-wm-themes', 'xfce4-xkb-plugin', 'xfce4-weather-plugin', 'xfce4-cpugraph-plugin',
                 'xfce4-battery-plugin', 'xfce4-wavelan-plugin', 'xfce4-clipman-plugin', 'xfce4-netload-plugin',
                 'xfce4-screenshooter-plugin', 'xfce4-pulseaudio-plugin'],
            Systems.Mageia:
                ['greybird-xfce4-theme', 'xfce4-screenshooter', 'xfce4-eyes-plugin', 'xfce4-clipman-plugin',
                 'xfce4-weather-plugin', 'xfce4-cpugraph-plugin', 'xfce4-xkb-plugin', 'xfce4-netload-plugin'],
            Systems.MxLinux:
                ['xfwm4-theme-breeze', 'xfce4-eyes-plugin'],
            Systems.Ubuntu:
                ['xfce4-wm-themes', 'xfce4-eyes-plugin'],
            Systems.Redhat:
                [],
            Systems.SuSE:
                # 'xfce4-wm-themes'
                ['xfce4-weather-plugin', 'xfce4-eyes-plugin', 'xfce4-clipman-plugin', 'xfce4-cpugraph-plugin',
                    'xfce4-screenshooter-plugin'],
        }
        return pkgs

    def getpkgs_xfce_programs(self):
        output('Collect XFCE programs...: ', False)
        if self.targetsys == Systems.Cygwin or self.subsys == Subsys.Windows:
            output('<tc>not necessary<nc>')
            return []
        if self.targetsys == Systems.SunOS or not self.options.desktop == 'xfce':
            output('<yellow>XFCE not used<nc>')
            return []
        if not flag_is_set(self.options, self.options.xfce, self.options.noxfce):
            output('<yellow>pass<nc>')
            return []
        result = self.pkg_xfce[Systems.Unknown] + self.pkg_xfce[self.targetsys]
        output('<green>Ok<nc>')
        return result

    def create_i3wm_packages(self):
        pkgs = {
            Systems.Unknown:
                ['i3', 'i3status', 'dmenu', 'xbacklight', 'feh', 'conky'],
            Systems.Arch:
                [],
            Systems.SunOS:
                [],
            Systems.Fedora:
                [],
            Systems.NetBSD or
            Systems.FreeBSD:
                [],
            Systems.Mageia:
                [],
            Systems.MxLinux:
                [],
            Systems.Redhat:
                [],
            Systems.SuSE:
                [],
        }
        return pkgs

    def getpkgs_i3wm_programs(self):
        output('Collect I3WM programs...: ', False)
        if self.targetsys == Systems.Cygwin or self.subsys == Subsys.Windows:
            output('<tc>not necessary<nc>')
            return []
        if self.targetsys == Systems.SunOS or not self.options.desktop == 'i3wm':
            output('<yellow>I3WM not used<nc>')
            return []
        if not flag_is_set(self.options, self.options.i3wm, self.options.noi3wm):
            output('<yellow>pass<nc>')
            return []
        result = self.pkg_i3wm[Systems.Unknown] + self.pkg_i3wm[self.targetsys]
        output('<green>Ok<nc>')
        return result

    def create_tex_packages(self):
        #    ['lyx'],
        pkgs = {
            Systems.Unknown:
                [],
            Systems.Arch:
                ['texmaker', 'latex2html', 'texstudio', 'texlive-music', 'texlive-langcyrillic', 'texlive-langjapanese'],
            Systems.SunOS:
                [],
            Systems.Fedora:
                ['texmaker', 'latex2html', 'texstudio', 'texlive-ctex', 'texlive-xecjk', 'texlive-babel-japanese',
                 'texlive-babel-russian', 'texlive-collection-music', 'texlive-xetex', 'texlive-cyrillic'],
            Systems.OpenBSD:
                ['texmaker', 'latex2html', 'texlive_texmf-full'],
            Systems.NetBSD:
                ['texmaker', 'latex2html', 'texstudio', 'font-cronyx-cyrillic', 'font-misc-cyrillic', 'font-screen-cyrillic',
                 'texlive-collection-all', 'font-screen-cyrillic', 'cyr-rfx-koi8-ru'],
            Systems.FreeBSD:
                ['texmaker', 'latex2html', 'texstudio', 'font-cronyx-cyrillic', 'font-misc-cyrillic', 'font-screen-cyrillic',
                 'texlive-full', 'xorg-fonts-cyrillic'],
            Systems.Mageia:
                ['texmaker', 'latex2html', 'texstudio', 'texlive-fonts-asian', 'texlive-fontsextra', 'texlive-collection-basic',
                 'texlive-context', 'texlive-dist', 'latex2html', 'texmaker', 'texstudio',
                 'x11-font-cyrillic', 'x11-font-cronyx-cyrillic', 'x11-font-screen-cyrillic'],
            Systems.MxLinux:
                ['texmaker', 'latex2html', 'texstudio', 'latexila', 'texlive-music', 'texlive-lang-cyrillic'],
            Systems.Ubuntu:
                ['texmaker', 'latex2html', 'texstudio', 'latexila', 'texlive-music', 'xfonts-cyrillic', 'latex-cjk-japanese',
                 't1-cyrillic', 'texlive-lang-cyrillic', 'texlive-fonts-extra'],
            Systems.Redhat:
                ['TeXmacs'],
            Systems.SuSE:
                ['texmaker', 'latex2html', 'texstudio', 'latexila', 'texlive-collection-music', 'texlive-cyrillic'],
        }
        return pkgs

    def getpkgs_tex(self):
        output('Collect TeX.............: ', False)
        if self.targetsys == Systems.Cygwin or self.subsys == Subsys.Windows:
            output('<tc>not necessary<nc>')
            return []
        if not flag_is_set(self.options, self.options.tex, self.options.notex):
            output('<yellow>pass<nc>')
            return []
        result = self.pkg_tex[Systems.Unknown] + self.pkg_tex[self.targetsys]
        output('<green>Ok<nc>')
        return result

    def create_games_packages(self):
        pkgs = {
            Systems.Unknown:
                [],
            Systems.Arch:
                ['xboard', 'pychess', 'chromium-bsu', 'dosbox', 'steam'],
            Systems.SunOS:
                ['nethack', 'freeciv', 'chromium-bsu'],
            Systems.Fedora:
                ['xboard', 'clonekeen', 'dreamchess', 'gnuchess'],
            Systems.OpenBSD:
                ['nethack', 'xboard', 'clonekeen', 'eboard', 'gnuchess', 'chromium-bsu', 'foobillard', 'xskat', 'speeddreams', 'kiten'],
            Systems.NetBSD:
                ['nethack-all', 'xboard', 'jin', 'eboard', 'gnuchess'],
            Systems.FreeBSD:
                ['xboard', 'crafty', 'foobillard', 'chessx', 'brutalchess', 'dreamchess'],
            Systems.Mageia:
                ['xboard', 'commandergenius', 'pychess', 'phalanx', 'dreamchess', 'gnuchess', 'xskat',
                 'yamagi-quake2', 'yamagi-quake2-xatrix', 'yamagi-quake2-rogue', 'chromium-bsu', 'speed-dreams', 'kiten'],
            Systems.MxLinux:
                ['xboard', 'phalanx', 'pychess', 'dosbox', 'xskat', 'crafty', 'glhack', 'slashem', 'quake', 'quake2'],
            Systems.Ubuntu:
                ['xboard', 'phalanx', 'pychess', 'dosbox'],
            Systems.Redhat:
                [],
            Systems.SuSE:
                ['xboard', 'phalanx', 'gnome-chess', 'gnuchess', 'lskat', 'kiten', 'steam']
        }
        return pkgs

    def getpkgs_games(self):
        output('Collect Games...........: ', False)
        if self.targetsys == Systems.Cygwin or self.subsys == Subsys.Windows:
            output('<tc>not necessary<nc>')
            return []
        if not flag_is_set(self.options, self.options.games, self.options.nogames):
            output('<yellow>pass<nc>')
            return []
        result = self.pkg_games[Systems.Unknown] + self.pkg_games[self.targetsys]
        output('<green>Ok<nc>')
        return result


    def create_nextcloud_packages(self):
        pkgs = {
            Systems.Unknown:
                [],
            Systems.Arch:
                ['nextcloud-client'],
            Systems.Fedora:
                ['nextcloud-client'],
            Systems.OpenBSD:
                ['nextcloudclient'],
            Systems.NetBSD:
                ['nextcloud-client'],
            Systems.FreeBSD:
                ['nextcloudclient'],
            Systems.Mageia:
                ['nextcloud-client'],
            Systems.MxLinux:
                ['nextcloud-desktop'],
            Systems.Ubuntu:
                ['nextcloud-client'],
            Systems.Redhat:
                ['nextcloud-client'],
            Systems.SuSE:
                ['nextcloud-client'],
        }
        return pkgs

    def getpkgs_nextcloud(self):
        output('Collect nextcloud.......: ', False)
        if self.targetsys == Systems.Cygwin or self.subsys == Subsys.Windows:
            output('<tc>not necessary<nc>')
            return []
        if not flag_is_set(self.options, self.options.nextcloud, self.options.nonextcloud):
            output('<yellow>pass<nc>')
            return []
        result = self.pkg_nextcloud[Systems.Unknown] + self.pkg_nextcloud[self.targetsys]
        output('<green>Ok<nc>')
        return result
    # if not get_pid('nextcloud'):
    #    subprocess.Popen('nextcloud')
