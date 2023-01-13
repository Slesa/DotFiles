# [11] Fedora             [15] RHEL/Alma       [14] SuSE
# [12] FreeBSD            [13] NetBSD
# [05] Xubuntu            [  ] MX              [16] Mageia
# [02] Ubuntu on Windows  [03] Cygwin          [  ] Arch / Manjaro
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

    if targetsys == Systems.Fedora or targetsys == Systems.Mageia:
        import os
        version = os.popen('rpm -E %fedora').read()[:-1]
        output(f'Fedora {version}')
        subprocess.check_call(['sudo', 'dnf', 'install', '-y', f'https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-{version}.noarch.rpm'])

    packages = ['zsh', 'neofetch']
    if subsys == Subsys.Origin:  # Not needed on Win Subsys
        packages += ['git', 'firefox']
    if targetsys == Systems.BSD or targetsys == Systems.NetBSD:
        packages += ['pidof', 'links', 'wget', 'rsync', 'bsdstats']
        if targetsys == Systems.BSD:
            packages += ['linux_base-c7', 'portmaster', 'portshaker']
    else:
        packages += ['vim', 'xsel']
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
        self.pkg_tex = self.create_tex_packages()
        self.pkg_games = self.create_games_packages()
        self.pkg_nextcloud = self.create_nextcloud_packages()

    def create_basic_packages(self):
        pkgs = {
            Systems.Unknown:
                ['zsh'],
            Systems.Arch:
                ['synergy', 'fortune-mod', 'zsh-lovers'],
            Systems.Fedora:
                ['fortune-mod', 'hfsutils', 'zsh-lovers', 'rdesktop', 'gcc-c++', 'synergy'],
            Systems.BSD:
                ['pstree', 'synergy', 'gitflow', 'keybase', 'fortune-mod-bofh'],
            Systems.Mageia:
                ['synergy', 'gitflow', 'fortune-mod', 'fortune-murphy'],
            Systems.MxLinux:
                ['git-flow', 'fortunes', 'fortunes-de'],
            Systems.Ubuntu:
                ['git-flow', 'fortunes', 'fortunes-de'],
            Systems.Redhat:
                ['fortune-mod', 'rdesktop', 'gcc-c++', 'synergy'],
            Systems.SuSE:
                # ['git-flow']
                ['fortune', 'hfsutils', 'synergy', 'qsynergy', 'rdesktop', 'gcc-c++', 'gcc']
        }
        if self.subsys== Subsys.Origin:
            pkgs[Systems.Ubuntu] += ['hfsplus', 'hfsutils', 'synergy', 'rdesktop']
        return pkgs

    def getpkgs_basics(self):
        output('Collect basics..........: ', False)
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
                ['curl', 'npm', 'mc', 'ncdu', 'htop', 'nmap'],
            Systems.Arch:
                ['links', 'w3m', 'postgresql', 'byobu', 'tmux', 'ranger', 'dos2unix', 'lshw', 'bacula-client', 'vim-pathogen'],
            Systems.Fedora:
                ['links', 'w3m', 'postgresql', 'byobu', 'postgresql-server', 'postgresql-contrib', 'tmux', 'bacula-client', 'bacula-console-bat',
                         'bacula-traymonitor'],
            Systems.BSD:
                # [xfce slim slim-themes]
                ['links', 'w3m', 'postgresql12-server', 'postgresql12-client', 'tmux', 'hs-pandoc', 'byobu', 'bacula11-client'],
            Systems.Mageia:
                ['links', 'w3m', 'postgresql13', 'postgresql13-server', 'tmux', 'ranger', 'dos2unix', 'openssh-server', 'byobu'],
            Systems.MxLinux:
                ['links', 'w3m', 'postgresql-11', 'tmux', 'ranger', 'dos2unix', 'openssh-server', 'vim-addon-manager',
                 'vim-pathogen', 'bacula-client', 'byobu'],
            Systems.Ubuntu:
                ['links', 'w3m', 'postgresql', 'byobu', 'tmux', 'ranger', 'dos2unix', 'vim-addon-manager', 'vim-pathogen'],
            Systems.Redhat:
                ['links', 'w3m', 'postgresql-server', 'postgresql-contrib', 'tmux', 'bacula-client'],
            Systems.SuSE:
                ['links', 'w3m', 'postgresql', 'byobu', 'tmux', 'ranger', 'dos2unix', 'dosemu'],
        }
        if self.subsys== Subsys.Origin:
            pkgs[Systems.Ubuntu] += ['synaptic', 'bacula-client', 'openssh-server', 'lshw']
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
                ['thunderbird', 'wmctrl', 'inkscape', 'audacity', 'gimp', 'bogofilter', 'hunspell', 'hexchat'],
            Systems.Arch:
                ['anthy', 'ibus-anthy', 'xaos', 'retext', 'chromium', 'mc', 'gvim', 'gnome-commander-git', 'file-commander-git', 'anki'],
            Systems.Fedora:
                ['anthy', 'ibus-anthy', 'xaos', 'gnome-commander', 'retext', 'chromium', 'vim-X11', 'gstreamer1-plugins-good',
                 'gstreamer1-plugins-bad-free', 'gstreamer1-plugins-bad-free-extras', 'unetbootin', 'anki',
                 'hunspell-de', 'hunspell-ru', 'hunspell-fr', 'hunspell-es'],
            Systems.BSD:
                ['xaos','vim-gtk3', 'vlc', 'gnupg', 'easytag', 'asunder', 'slim', 'slim-themes',
                 'vim-gtk3', 'chromium', 'vlc', 'gnupg', 'unetbootin', 'de-hunspell', 'ru-hunspell', 'fr-hunspell', 'es-hunspell',
                 'ja-font-kochi', 'ja-ibus-anthy', 'lollypop', 'easytag', 'asunder', 'vscode',
                 'ghostwriter', 'xorg', 'slim', 'slim-themes', 'xpdf'
                 ],
                # ['chromium', 'unetbootin', 'vscode', 'lollypop', 'ghostwriter', 'anki', 'ja-font-kochi', 'ja-ibus-anthy', 'xorg',
                #   'de-hunspell', 'ru-hunspell', 'fr-hunspell', 'es-hunspell']
            Systems.Mageia:
                ['anthy', 'ibus-anthy', 'xaos', 'chromium-browser', 'vim-X11', 'vlc', 'gnome-commander', 'unetbootin', 'rhythmbox', 'anki',
                 'hunspell-de', 'hunspell-es', 'hunspell-ru', 'hunspell-fr',
                 'fonts-ttf-japanese', 'fonts-ttf-japanese-extra', 'google-noto-sans-cjk-jp-fonts', 'google-noto-sans-jp-fonts', 'google-noto-serif-jp-fonts', 'google-noto-serif-cjk-jp-fonts'
                 ],
            Systems.MxLinux:
                ['anthy', 'ibus-anthy', 'xaos', 'vim-gtk', 'retext', 'vlc', 'tuxcmd', 'gpgv2', 'hunspell-ru', 'hunspell-fr', 'hunspell-es', 'anki',
                 'hunspell-de-de', 'chromium'],
            Systems.Ubuntu:
                ['anthy', 'ibus-anthy', 'xaos', 'vim-gtk', 'retext', 'vlc', 'tuxcmd', 'gpgv2', 'hunspell-ru', 'hunspell-fr', 'hunspell-es', 'anki',
                 'hunspell-de', 'chromium-browser'],
            Systems.Redhat:
                ['anthy', 'ibus-anthy', 'chromium', 'vim-X11', 'gstreamer1-plugins-good', 'gstreamer1-plugins-bad-free',
                 'hunspell-de', 'hunspell-ru', 'hunspell-fr', 'hunspell-es'],
            Systems.SuSE:
                ['anthy', 'ibus-anthy', 'xaos', 'chromium', 'gvim', 'vlc', 'gnome-commander', 'retext', 'unetbootin', 'rhythmbox'], #, 'anki']
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
        output('<green>Ok<nc>')
        return result

    def create_compiler_packages(self):
        pkgs = {
            Systems.Unknown:
                ['meld', 'cgdb', 'gdb', 'cmake', 'ccache'],
            Systems.Arch:
                ['qt5', 'nodejs', 'yarn'],
            Systems.Fedora:
                ['ncurses-devel', 'cmake-gui', 'nodejs', 'mesa-libGL', 'mesa-libGL-devel'],
            Systems.BSD:
                # ['fsharp', 'mono', ]
                ['qt5-designer', 'qtcreator', 'node16', 'npm', 'yarn', 'openjdk14'],
            Systems.Mageia:
                ['cmake-qtgui', 'nodejs', 'lib64mesagl-devel'],
            Systems.MxLinux:
                ['python3-venv', 'mono-complete', 'cmake-qt-gui', 'yarnpkg', 'pyqt5-dev', 'pyqt5-examples',
                 'qt5-default', 'qtbase5-dev', 'libgl1-mesa-dev', 'libglu1-mesa-dev'],
            Systems.Ubuntu:
                # [ 'fsharp', ]
                ['qt5-default', 'nodejs', 'yarn'],
            Systems.Redhat:
                ['ncurses-devel', 'cmake-gui', 'nodejs', 'mesa-libGL', 'mesa-libGL-devel'
                    , 'dotnet', 'dotnet-sdk-6.0', 'dotnet-templates-6.0'],
            Systems.SuSE:
                # ['mono-complete','fsharp',]
                ['nodejs19', 'yarn', 'cmake-gui'],
        }
        return pkgs

    def getpkgs_compiler(self):
        output('Collect compiler........: ', False)
        if self.targetsys == Systems.Cygwin or self.subsys == Subsys.Windows:
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
                ['xfce4-wm-themes', 'xfce4-xkb-plugin', 'xfce4-weather-plugin', 'xfce4-cpugraph-plugin',
                 'xfce4-battery-plugin', 'xfce4-wavelan-plugin', 'xfce4-clipman-plugin', 'xfce4-netload-plugin',
                 'xfce4-screenshooter-plugin', 'xfce4-pulseaudio-plugin'],
            Systems.Fedora:
                ['xfwm4-themes', 'xfce4-eyes-plugin'],
            Systems.BSD:
                ['xfce4-wm-themes', 'xfce4-xkb-plugin', 'xfce4-weather-plugin', 'xfce4-cpugraph-plugin',
                 'xfce4-battery-plugin', 'xfce4-wavelan-plugin', 'xfce4-clipman-plugin', 'xfce4-netload-plugin',
                 'xfce4-screenshooter-plugin', 'xfce4-pulseaudio-plugin'],
            Systems.Mageia:
                ['greybird-xfce4-theme', 'xfce4-screenshooter', 'xfce4-eyes-plugin', 'xfce4-clipman-plugin',
                 'xfce4-weather-plugin', 'xfce4-cpugraph-plugin', 'xfce4-xkb-plugin', 'xfce4-netload-plugin'],
            Systems.MxLinux:
                ['xfce4-wm-themes', 'xfce4-eyes-plugin'],
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
        if not self.options.desktop == 'xfce':
            output('<yellow>XFCE not used<nc>')
            return
        if not flag_is_set(self.options, self.options.xfce, self.options.noxfce):
            output('<yellow>pass<nc>')
            return []
        result = self.pkg_xfce[Systems.Unknown] + self.pkg_xfce[self.targetsys]
        output('<green>Ok<nc>')
        return result

    def create_tex_packages(self):
        pkgs = {
            Systems.Unknown:
                ['lyx'],
            Systems.Arch:
                ['texmaker', 'latex2html', 'texstudio', 'texlive-music', 'texlive-langcyrillic', 'texlive-langjapanese'],
            Systems.Fedora:
                ['texmaker', 'latex2html', 'texstudio', 'texlive-ctex', 'texlive-xecjk', 'texlive-babel-japanese',
                 'texlive-babel-russian', 'texlive-collection-music', 'texlive-xetex', 'texlive-cyrillic'],
            Systems.BSD:
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
                ['xboard', 'pychess', 'chromium-bsu', 'dosbox'],
            Systems.Fedora:
                ['xboard', 'clonekeen', 'dreamchess', 'gnuchess'],
            Systems.BSD:
                ['xboard', 'crafty', 'foobillard', 'pouetchess', 'chessx', 'brutalchess', 'dreamchess'],
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
            Systems.BSD:
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
