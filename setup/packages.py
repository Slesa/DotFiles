from setup.osplatform import Systems, Subsys
from setup.console import output
from setup.helpers import flag_is_set, install


# [11] Fedora             [12] FreeBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin
# [  ] SuSE               [  ] Arch / Manjaro
def install_core(installprog, targetsys, subsys, options):
    output('Collect core............: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.core, options.nocore):
        output('<yellow>pass<nc>')
        return
    packages = ['zsh']
    if subsys == Subsys.Origin:  # Not needed on Win Subsys
        packages += ['vim', 'git', 'firefox']
    if targetsys == Systems.BSD:
        packages += ['pidof', 'links', 'wget', 'rsync', 'bsdstats', 'linux_base-c7', 'portmaster']
    else:
        packages += ['vim', 'xsel']
    install(installprog, packages)
    output('<green>Ok<nc>')


# [11] Fedora             [12] FreeBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin
# [  ] SuSE               [  ] Arch / Manjaro
def getpkgs_basics(targetsys, subsys, options):
    output('Collect basics..........: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return []
    if not flag_is_set(options, options.basics, options.nobasics):
        output('<yellow>pass<nc>')
        return []
    packages = ['zsh']
    if targetsys == Systems.BSD:
        # packages += ['vscode']
        packages += ['gitflow', 'fortune-mod-bofh', 'pstree', 'synergy', 'keybase']
    elif targetsys == Systems.MxLinux:
        packages += ['git-flow', 'fortunes', 'fortunes-de']
    elif targetsys == Systems.Ubuntu or targetsys == Systems.Zorin:
        packages += ['git-flow', 'fortunes', 'fortunes-de']
        if subsys == Subsys.Origin:
            packages += ['hfsplus', 'hfsutils', 'synergy', 'rdesktop']
    elif targetsys == Systems.SuSE:
        packages += ['git-flow', 'fortune', 'hfsutils', 'synergy', 'qsynergy', 'rdesktop', 'gcc-c++', 'gcc']
    elif targetsys == Systems.Arch:
        packages += ['synergy', 'fortune-mod', 'zsh-lovers']
    elif targetsys == Systems.Fedora:
        packages += ['fortune-mod', 'hfsutils', 'zsh-lovers', 'rdesktop', 'gcc-c++', 'synergy']
    output('<green>Ok<nc>')
    return packages


# [11] Fedora             [12] FreeBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin
# [  ] SuSE               [  ] Arch / Manjaro
def getpkgs_programs(targetsys, subsys, options):
    # Ubuntu: tmuxinator, tmux-plugin-manager ranger
    output('Collect programs........: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return []
    if not flag_is_set(options, options.programs, options.noprograms):
        output('<yellow>pass<nc>')
        return []
    packages = ['curl', 'npm', 'mc', 'w3m', 'links', 'ncdu', 'htop', 'nmap', 'byobu']
    if targetsys == Systems.BSD:
        # fehlt: xfce slim slim-themes
        packages += ['postgresql12-server', 'postgresql12-client', 'tmux', 'bacula11-client', 'hs-pandoc', ]
    elif targetsys == Systems.MxLinux:
        packages += ['postgresql-11', 'tmux', 'ranger', 'dos2unix', 'openssh-server', 'vim-addon-manager',
                     'vim-pathogen', 'bacula-client']
    else:
        packages += ['postgresql']
        if targetsys == Systems.Ubuntu or targetsys == Systems.Zorin:
            # 'tmuxp', 'tmuxinator', 'tmux-plugin-manager'
            packages += ['tmux', 'ranger', 'dos2unix', 'vim-addon-manager', 'vim-pathogen']
            if subsys == Subsys.Origin:
                packages += ['synaptic', 'bacula-client', 'openssh-server', 'lshw']
        elif targetsys == Systems.SuSE:
            packages += ['tmux', 'dosemu', 'dos2unix', 'ranger']
        elif targetsys == Systems.Arch:
            packages += ['tmux', 'lshw', 'ranger', 'dos2unix', 'bacula-client', 'vim-pathogen']
        elif targetsys == Systems.Fedora:
            packages += ['postgresql-server', 'postgresql-contrib', 'tmux', 'bacula-client', 'bacula-console-bat',
                         'bacula-traymonitor']
    output('<green>Ok<nc>')
    return packages


# [11] Fedora             [12] FreeBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin
# [  ] SuSE               [  ] Arch / Manjaro
def getpkgs_xprograms(targetsys, subsys, options):
    # Ubuntu: xaos, guake
    output('Collect X programs......: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return []
    if not flag_is_set(options, options.xprograms, options.noxprograms):
        output('<yellow>pass<nc>')
        return []
    # 'devilspie2', 'cawbird',
    packages = ['xaos', 'thunderbird', 'wmctrl', 'inkscape', 'audacity', 'gimp', 'bogofilter', 'hunspell', 'anki',
                'hexchat']
    if targetsys == Systems.BSD:
        packages += ['vim-gtk3', 'chromium', 'vlc', 'gnupg', 'unetbootin',
                     'de-hunspell', 'ru-hunspell', 'fr-hunspell', 'es-hunspell',
                     'ja-font-kochi', 'ja-ibus-anthy', 'lollypop', 'easytag', 'asunder', 'vscode',
                     'ghostwriter', 'xorg', 'slim', 'slim-themes']
    elif targetsys == Systems.Ubuntu or targetsys == Systems.Zorin or targetsys == Systems.MxLinux:
        if targetsys == Systems.Zorin or targetsys == Systems.MxLinux:
            packages += ['hunspell-de-de']
        else:
            packages += ['hunspell-de']
        if targetsys == Systems.MxLinux:
            packages += ['chromium']
        else:
            packages += ['chromium-browser']
        packages += ['vim-gtk', 'retext', 'vlc', 'tuxcmd', 'gpgv2', 'hunspell-ru', 'hunspell-fr', 'hunspell-es']
    elif targetsys == Systems.SuSE:
        packages += ['chromium', 'gvim', 'vlc', 'tuxcmd', 'retext', 'unetbootin']
    elif targetsys == Systems.Arch:
        packages += ['retext', 'chromium', 'mc', 'gvim', 'gnome-commander-git', 'file-commander-git']
    elif targetsys == Systems.Fedora:
        packages += ['gnome-commander', 'retext', 'chromium', 'vim-X11', 'gstreamer1-plugins-good',
                     'gstreamer1-plugins-bad-free', 'gstreamer1-plugins-bad-free',
                     'gstreamer1-plugins-bad-free-extras', 'unetbootin',
                     'hunspell-de', 'hunspell-ru', 'hunspell-fr', 'hunspell-es']
        # ['streamer1-plugins-base', 'gstreamer1-plugins-ugly','gstreamer1-plugins-bad-freeworld','ffmpeg']
    output('<green>Ok<nc>')
    return packages


# [11] Fedora             [12] FreeBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin
# [  ] SuSE               [  ] Arch / Manjaro
def getpkgs_compiler(targetsys, subsys, options):
    output('Install compiler........: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return []
    if not flag_is_set(options, options.compiler, options.nocompiler):
        output('<yellow>pass<nc>')
        return []
    packages = ['meld', 'cgdb', 'gdb', 'cmake', 'ccache']
    if targetsys == Systems.BSD:
        packages += ['qt5-designer', 'qtcreator'
                     'fsharp', 'mono', 'node14', 'npm', 'yarn', 'openjdk14']
    elif targetsys == Systems.Ubuntu or targetsys == Systems.Zorin:
        packages += ['qt5-default', 'fsharp', 'mono-complete', 'nodejs', 'yarn']
    elif targetsys == Systems.SuSE:
        packages += ['fsharp', 'mono-complete', 'cmake-gui', 'kdevelop5', 'kdevelop5-pg-qt']
    elif targetsys == Systems.Arch:
        packages += ['qt5', 'mono', 'mono-tools', 'nodejs', 'yarn']
    elif targetsys == Systems.Fedora:
        packages += ['mono-complete', 'ncurses-devel', 'cmake-gui', 'nodejs', 'mesa-libGL', 'mesa-libGL-devel']
        # , 'yarn']
    elif targetsys == Systems.MxLinux:
        packages += ['python3-venv', 'mono-complete', 'cmake-qt-gui', 'yarnpkg', 'pyqt5-dev', 'pyqt5-examples',
                     'qt5-default', 'qtbase5-dev', 'libgl1-mesa-dev', 'libglu1-mesa-dev']
    output('<green>Ok<nc>')
    return packages


# [11] Fedora             [12] FreeBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin
# [  ] SuSE               [  ] Arch / Manjaro
def getpkgs_xfce_programs(targetsys, subsys, options):
    output('Collect XFCE programs...: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return []
    if not options.desktop == 'xfce':
        output('<yellow>XFCE not used<nc>')
        return
    if not flag_is_set(options, options.xfce, options.noxfce):
        output('<yellow>pass<nc>')
        return []
    packages = ['xfce4-wm-themes']
    if targetsys == Systems.BSD or targetsys == Systems.Arch:
        packages = ['xfce4-xkb-plugin', 'xfce4-weather-plugin', 'xfce4-screenshooter-plugin', 'xfce4-cpugraph-plugin',
                    'xfce4-battery-plugin', 'xfce4-wavelan-plugin', 'xfce4-clipman-plugin', 'xfce4-netload-plugin',
                    'xfce4-pulseaudio-plugin']
    elif targetsys == Systems.Ubuntu or targetsys == Systems.Zorin or targetsys == Systems.Fedora or targetsys == Systems.MxLinux:
        packages = ['xfce4-eyes-plugin']
    # elif targetsys == Systems.SuSE:
    #    packages += ['']
    # elif targetsys == Systems.Arch:
    #    packages += ['']
    # elif targetsys == Systems.Fedora:
    #    packages += ['']
    output('<green>Ok<nc>')
    return packages


# [11] Fedora             [12] FreeBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin
# [  ] SuSE               [  ] Arch / Manjaro
def getpkgs_tex(targetsys, subsys, options):
    output('Collect TeX.............: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return []
    if not flag_is_set(options, options.tex, options.notex):
        output('<yellow>pass<nc>')
        return []
    packages = ['texmaker', 'lyx', 'latex2html', 'texstudio']
    if targetsys == Systems.BSD:
        # 'latexila',
        packages += ['texlive-full', 'font-cronyx-cyrillic', 'font-misc-cyrillic', 'font-screen-cyrillic',
                     'xorg-fonts-cyrillic']
    elif targetsys == Systems.MxLinux:
        packages += ['latexila', 'texlive-music', 'texlive-lang-cyrillic']
    elif targetsys == Systems.Ubuntu or targetsys == Systems.Zorin:
        packages += ['latexila', 'texlive-music', 'xfonts-cyrillic', 'latex-cjk-japanese', 't1-cyrillic',
                     'texlive-lang-cyrillic', 'texlive-fonts-extra']
    elif targetsys == Systems.SuSE:
        packages += ['latexila', 'texlive-collection-music', 'texlive-cyrillic']
    elif targetsys == Systems.Arch:
        packages += ['texlive-music', 'texlive-langcyrillic', 'texlive-langjapanese']
    elif targetsys == Systems.Fedora:
        packages += ['texlive-ctex', 'texlive-xecjk', 'texlive-babel-japanese', 'texlive-babel-russian', 'texlive-collection-music' 'texlive-xetex', 'texlive-cyrillic', 'texlive-collection-music']
    output('<green>Ok<nc>')
    return packages


# [11] Fedora             [12] FreeBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin
# [  ] SuSE               [  ] Arch / Manjaro
def getpkgs_games(targetsys, subsys, options):
    output('Collect Games...........: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return []
    if not flag_is_set(options, options.games, options.nogames):
        output('<yellow>pass<nc>')
        return []
    packages = ['xboard']
    if targetsys == Systems.BSD:
        packages += ['crafty', 'dreamchess', 'brutalchess', 'chessx', 'pouetchess']
        packages += ['foobillard']
    elif targetsys == Systems.MxLinux:
        packages += ['phalanx', 'pychess', 'dosbox', 'xskat', 'crafty', 'glhack', 'slashem', 'quake', 'quake2']
    elif targetsys == Systems.Ubuntu or targetsys == Systems.Zorin:
        packages += ['phalanx', 'pychess', 'dosbox']
    elif targetsys == Systems.SuSE:
        packages += ['phalanx', 'gnome-chess', 'gnuchess', 'lskat kiten']
    elif targetsys == Systems.Arch:
        packages += ['pychess', 'chromium-bsu', 'dosbox']
    elif targetsys == Systems.Fedora:
        packages += ['clonekeen', 'dreamchess', 'gnuchess']
    output('<green>Ok<nc>')
    return packages


# [11] Fedora             [12] FreeBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin
# [  ] SuSE               [  ] Arch / Manjaro
def getpkgs_nextcloud(targetsys, subsys, options):
    output('Collect nextcloud.......: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return []
    if not flag_is_set(options, options.nextcloud, options.nonextcloud):
        output('<yellow>pass<nc>')
        return []
    if targetsys == Systems.MxLinux:
        packages = ['nextcloud-desktop']
    elif targetsys == Systems.BSD:
        packages = ['nextcloudclient']
    else:
        packages = ['nextcloud-client']
    output('<green>Ok<nc>')
    return packages
    # if not get_pid('nextcloud'):
    #    subprocess.Popen('nextcloud')
