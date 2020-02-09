# 0.2 - Ubuntu on Windows
import os
import platform
import subprocess
from pathlib import Path
from enum import Enum

# Keybase, Renoise, mp3 (-verwaltung), GitKraken?, XMind

Basepath = str(Path.home()) + '/.dotfiles'

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
def get_pid(name):
    try:
        return subprocess.check_output(["pidof", "-s", name])
    except subprocess.CalledProcessError:
        return 0

#region Output

Colors = [
    ('<red>', '\033[0;31m'),
    ('<green>', '\033[0;32m'),
    ('<yellow>', '\033[0;33m'),
    ('<head>', '\033[0;35m'),
    ('<tc>', '\033[0;33m'),
    ('<nc>', '\033[0m')]

def output(msg, cr=True):
    buffer = msg
    for idx,col in enumerate(Colors):
        buffer = buffer.replace(col[0], col[1])
    if cr:
        print(buffer)
    else:
        print(buffer, end='')

#endregion

#region Parser

def create_parser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--desktop', default='xfce', choices=['kde', 'gnome'])
    parser.add_argument('--full', action='store_true')
    parser.add_argument('--zsh', action='store_true')
    parser.add_argument('--nozsh', action='store_true')
    parser.add_argument('--login', action='store_true')
    parser.add_argument('--nologin', action='store_true')
    parser.add_argument('--links', action='store_true')
    parser.add_argument('--nolinks', action='store_true')
    parser.add_argument('--core', action='store_true')
    parser.add_argument('--nocore', action='store_true')
    parser.add_argument('--owncube', action='store_true')
    parser.add_argument('--noowncube', action='store_true')
    parser.add_argument('--dotfiles', action='store_true')
    parser.add_argument('--nodotfiles', action='store_true')
    parser.add_argument('--basics', action='store_true')
    parser.add_argument('--nobasics', action='store_true')
    parser.add_argument('--programs', action='store_true')
    parser.add_argument('--noprograms', action='store_true')
    parser.add_argument('--xprograms', action='store_true')
    parser.add_argument('--noxprograms', action='store_true')
    parser.add_argument('--compiler', action='store_true')
    parser.add_argument('--nocompiler', action='store_true')
    parser.add_argument('--xfce', action='store_true')
    parser.add_argument('--noxfce', action='store_true')
    parser.add_argument('--tex', action='store_true')
    parser.add_argument('--notex', action='store_true')
    parser.add_argument('--games', action='store_true')
    parser.add_argument('--nogames', action='store_true')
    parser.add_argument('--fonts', action='store_true')
    parser.add_argument('--nofonts', action='store_true')
    parser.add_argument('--clone', action='store_true')
    parser.add_argument('--noclone', action='store_true')
    parser.add_argument('--github', action='store_true')
    parser.add_argument('--nogithub', action='store_true')
    parser.add_argument('--gitlab', action='store_true')
    parser.add_argument('--nogitlab', action='store_true')
    #parser.add_argument('--externals', action='store_true')
    parser.add_argument('--noexternals', action='store_true')
    parser.add_argument('--qt', action='store_true')
    parser.add_argument('--noqt', action='store_true')
    parser.add_argument('--rider', action='store_true')
    parser.add_argument('--norider', action='store_true')
    parser.add_argument('--pycharm', action='store_true')
    parser.add_argument('--nopycharm', action='store_true')
    result = parser.parse_args()
    return result

#endregion

#region Operating System

class Systems(Enum):
  Unknown = 0
  Cygwin = 1
  MacOS = 2
  BSD = 3
  Fedora = 4
  SuSE = 5
  Arch = 6
  Ubuntu = 7
class Subsys(Enum):
  Origin = 0
  Windows = 1

def determine_os():
    output(f'System..................: <green>{platform.system()}<nc>')
    # [ ] cygwin                    [ ] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.1] Ubuntu
    # [ ] Fedora                    [ ] Mint
    
    release =  platform.release().lower()
    subsys = Subsys.Windows if 'microsoft' in release else Subsys.Origin
    output('Found...................: ', False)
    system = platform.system().lower()
    if system.startswith('cygwin'):
        output('<green>CygWin<nc>')
        return (Systems.Cygwin,subsys)
    if system == 'darwin':
        output('<green>MacOS<nc>')
        return (Systems.MacOs,subsys)
    if 'bsd' in system:
        output('<green>BSD derivate<nc>')
        return (Systems.BSD,subsys)
    if system == 'linux':
        linux = platform.platform().lower()
        if 'fedora' in linux:
            output('<green>Fedora<nc>')
            return (Systems.Fedora,subsys)
        if 'suse' in linux:
            output('<green>SuSE<nc>')
            return (Systems.SuSE,subsys)
        if 'arch' in linux:
            output('<green>Arch / Manjaro<nc>')
            return (Systems.Arch,subsys)
        if 'ubuntu' in linux:
            output(f'<green>Ubuntu {subsys}<nc>')
            return (Systems.Ubuntu,subsys)
    output('<red>Unknown<nc>')
    output(f'Platform................: <yellow>{platform.platform()}<nc>')
    output(f'Release.................: <yellow>{platform.release()}<nc>')
    output(f'Version.................: <yellow>{platform.version()}<nc>')
    #output(f'Uname...................: <yellow>{str(platform.uname())}<nc>')
    output(f'Distribution............: <yellow>{platform.linux_distribution()[0]}<nc>')
    return (None,subsys)

def determine_installer(os):
    if os == Systems.BSD:
        return ["sudo", "pkg", "install", "-y"]
    if os == Systems.Fedora:
        return ["sudo", "yum", "install", "-y"]
    if os == Systems.SuSE:
        return ["sudo", "zypper", "install", "-ly"]
    if os == Systems.Arch:
        return ["sudo", "pacman", "--noconfirm", "-Syu"]
    if os == Systems.Ubuntu:
        return ["sudo", "apt-get", "install", "-y"]
    return None

#endregion

#region Helpers

def copy_text_to_clipboard(os, text):
    if os == Systems.MacOS:
        subprocess.Popen(('pbcopy', text))
    elif os == Systems.Cygwin:
        subprocess.run(f'echo {text} > /dev/clipboard')
    else:
        subprocess.Popen(('xsel', '--clipboard', text))
        #cat = subprocess.Popen(('echo', f'"{text}"'), stdout=subprocess.PIPE)
        #output = subprocess.check_output(('xsel', '--clipboard'), stdin=cat.stdout)
        #cat.wait()
        #subprocess.run(['cat', '"{text}"', '\|', 'xsel', '--clipboard'])

def ensure_root(osys):
    import getpass
    output('Checking root access....: ', False)
    if osys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return

    if not os.geteuid()==0:
        #output('<yellow>have to ask<nc>')
        #sudopw = getpass.getpass('Enter sudo password.....: ')
        sudopw = getpass.getpass()
        command = 'ls > /dev/null'
        os.system('echo %s|sudo -S %s' % (sudopw, command))
    #subprocess.Popen('sudo', shell=True)
    output('<green>Ok<nc>')

#endregion

def install(installprog, packages):
    print (installprog)
    print (packages)
    subprocess.check_call(installprog + packages)

def flag_is_set(options, on_flag, off_flag):
  if on_flag:
    return True
  if options.full and not off_flag:
    return True
  return False

def install_core(targetsys, subsys, installprog, options):
    # [ ] cygwin                    [ ] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.1] Ubuntu
    # [ ] Fedora                    [ ] Mint
    output('Install core............: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.core, options.nocore):
        output('<yellow>pass<nc>')
        return
    packages = ['xsel', 'vim', 'zsh']
    if subsys == Subsys.Origin: # Not needed on Win Subsys
        packages += ['git', 'firefox']
    if targetsys == Systems.BSD:
        packages += ['pidof']
    output('<green>Ok<nc>')
    install(installprog, packages)
    output('Core installation.......: <green>Done<nc>')


def install_zsh(targetsys, options):
    # [ ] cygwin                    [ ] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.1] Ubuntu
    # [ ] Fedora                    [ ] Mint
    output('Install Zsh.............: ', False)
    if not flag_is_set(options, options.zsh, options.nozsh):
        output('<yellow>pass<nc>')
        return
    targetfile = str(Path.home()) + '/.zshrc'
    if os.path.isfile(targetfile):
        output('<green>already installed<nc>')
    else:
        output('<tc>copying<nc>')
        srcfile = 'zshrc.cygwin'
        if targetsys == Systems.Cygwin:
            srcfile = 'zshrc.cygwin'
        elif targetsys == Systems.BSD:
            srcfile = 'zshrc.freebsd'
        elif targetsys == Systems.Fedora:
            srcfile = 'zshrc.fedora'
        elif targetsys == Systems.Ubuntu:
            srcfile = 'zshrc.ubuntu'
        subprocess.check_call(['cp', Basepath + '/data/templ/' + srcfile, targetfile])
        output('zshrc installed.........: <green>Done<nc>')
    output('set zsh shell...........: ', False)
    currentshell = os.popen('echo $SHELL').read()
    if 'zsh' in currentshell:
        output('<yellow>already set<nc>')
    else:
      shell = os.popen('which zsh').read()[:-1]
      subprocess.check_call(['chsh', '-s', shell])
      output('<green>Done<nc>')


def install_dotfiles(options):
    # [ ] cygwin                    [ ] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.1] Ubuntu
    # [ ] Fedora                    [ ] Mint
    output('Install dotfiles........: ', False)
    if not flag_is_set(options, options.dotfiles, options.nodotfiles):
        output('<yellow>pass<nc>')
        return
    if os.path.isdir(Basepath):
        output('<green>already installed<nc>')
        subprocess.check_call(['git', 'pull', 'origin', 'master'])
        return
    output('<tc>cloning<nc>')
    subprocess.check_call(['git', 'clone', 'git@github.com:slesa/DotFiles', Basepath])
    output('Dotfiles installed......: <green>Done<nc>')


def install_login(targetsys, subsys, options):
    # [ ] cygwin                    [ ] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.1] Ubuntu
    # [ ] Fedora                    [ ] Mint
    output('Install Login...........: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.zsh, options.nozsh):
        output('<yellow>pass<nc>')
        return
    targetdir = '/usr/share/backgrounds/'
    targetfile = 'StarTrekLogo1920x1080.jpg'
    if targetsys == Systems.SuSE or targetsys == Systems.Fedora:
        targetdir = '/usr/share/wallpapers/'
    elif targetsys == Systems.BSD:
        targetdir = '/usr/local/share/backgrounds/'
    if not os.path.isfile(targetdir + targetfile):
        subprocess.check_call(['sudo', 'cp', Basepath + '/data/img/' + targetfile, targetdir + targetfile])
        subprocess.check_call(['sudo', 'chmod', '+r', targetdir + targetfile])
        if options.desktop=='xfce':
            if not targetsys == Systems.BSD:
                subprocess.check_call(['sudo', 'sed', '+i', "'/background=/c\background=/usr/share/wallpapers/StarTrekLogo1920x1080.jpg'", '/etc/lightdm/lightdm-gtk-greeter.conf' ])
            else:
                subprocess.check_call(['sudo', 'sed', '+i', '-e', '"s/BACKGROUND_IMAGE=.*/BACKGROUND_IMAGE=StarTrekLogo1920x1080.jpg/g"', '/usr/local/share/PCDM/themes/trueos/trueos.theme' ])

    output('<green>Ok<nc>')


def install_links(targetsys, subsys, options):
    # [ ] cygwin                    [ ] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.1] Ubuntu
    # [ ] Fedora                    [ ] Mint
    output('Install Links...........: ', False)
    if not flag_is_set(options, options.links, options.nolinks):
        output('<yellow>pass<nc>')
        return
    bindir = str(Path.home()) + '/bin'
    if not os.path.isdir(bindir):
        os.mkdir(bindir)
    if not os.path.islink(bindir+'/tools'):
        os.symlink(Basepath + '/bin/tools', bindir+'/tools')

    zshfile = str(Path.home()) + '/.zsh'
    if not os.path.islink(zshfile):
        os.symlink(Basepath + '/etc/unix/zsh', zshfile)
    tmuxfile = str(Path.home()) + '/.tmux.conf'
    if not os.path.islink(tmuxfile):
        os.symlink(Basepath + '/etc/unix/tmux.conf', tmuxfile)
    gitfile = str(Path.home()) + '/.gitconfig'
    if not os.path.islink(gitfile):
        os.symlink(Basepath + '/etc/unix/gitconfig', gitfile)
    vimfile = str(Path.home()) + '/.vimrc'
    if not os.path.islink(vimfile):
        os.symlink(Basepath + '/etc/unix/vimrc', vimfile)

    if not targetsys==Systems.Cygwin and not subsys == Subsys.Windows:
        autosource = Basepath + '/etc/unix/autostart/'
        autostart = str(Path.home()) + '/.config/autostart/'
        if not os.path.isdir(autostart):
            os.mkdir(autostart)
        autoOwnCloud = 'ownCloud.desktop'
        if not os.path.isfile(autostart + autoOwnCloud):
            os.symlink(autosource + autoOwnCloud, autostart + autoOwnCloud)
        autoThunderbird = 'Thunderbird.desktop'
        if not os.path.isfile(autostart + autoThunderbird):
            os.symlink(autosource + autoThunderbird, autostart + autoThunderbird)
    output('<green>Ok<nc>')


def install_owncube(targetsys, subsys, installprog, options):
    # [ ] cygwin                    [ ] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.1] Ubuntu
    # [ ] Fedora                    [ ] Mint
    output('Install owncube.........: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.owncube, options.noowncube):
        output('<yellow>pass<nc>')
        return
    packages = ['owncloud-client']  if not targetsys == Systems.BSD else ['owncloudclient']
    output('<green>Ok<nc>')
    install(installprog, packages)
    output('Owncube installation....: <green>Done<nc>')

    if not get_pid('owncloud'):
        subprocess.Popen('owncloud')

#createSshKey

def install_basics(targetsys, subsys, installprog, options):
    # [ ] cygwin                    [ ] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.1] Ubuntu
    # [ ] Fedora                    [ ] Mint
    output('Install basics..........: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.basics, options.nobasics):
        output('<yellow>pass<nc>')
        return
    packages = ['zsh']
    if targetsys == Systems.BSD:
        packages += ['gitflow', 'fortune-mod-bofh', 'pstree', 'inxi', 'synergy']
    elif targetsys == Systems.Ubuntu:
        packages += ['git-flow', 'fortunes', 'fortunes-de']
        if subsys==Subsys.Origin:
          packages += ['hfsplus', 'hfsutils', 'synergy', 'rdesktop']
    elif targetsys == Systems.SuSE:
        packages += ['git-flow', 'fortune', 'hfsutils', 'synergy', 'qsynergy', 'rdesktop', 'gcc-c++', 'gcc']
    elif targetsys == Systems.Arch:
        packages += ['synergy', 'fortune-mod', 'zsh-lovers']
    elif targetsys == Systems.Fedora:
        packages += ['fortune-mod', 'hfsutils', 'gitflow', 'zsh-lovers', 'rdesktop', 'gcc-c++', 'synergy']
    output('<green>Ok<nc>')
    install(installprog, packages)
    output('Basic installation......: <green>Done<nc>')

# Ubuntu: tmuxinator, tmux-plugin-manager ranger
def install_programs(targetsys, subsys, installprog, options):
    # [ ] cygwin                    [ ] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.1] Ubuntu
    # [ ] Fedora                    [ ] Mint
    output('Install programs........: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.programs, options.noprograms):
        output('<yellow>pass<nc>')
        return
    packages = ['curl', 'npm', 'mc', 'w3m', 'links', 'ncdu', 'htop', 'nmap']
    if targetsys == Systems.BSD:
        # fehlt: xfce slim slim-themes
        packages += ['mux', 'bacula-client', 'txorg']
    elif targetsys == Systems.Ubuntu:
        # 'tmuxp', 'tmuxinator', 'tmux-plugin-manager'
        packages += ['ranger', 'dos2unix', 'vim-addon-manager', 'vim-pathogen']
        if subsys == Subsys.Origin:
            packages += ['synaptic', 'bacula-client', 'openssh-server', 'lshw']
    elif targetsys == Systems.SuSE:
        packages += ['tmux', 'dosemu', 'dos2unix', 'ranger']
    elif targetsys == Systems.Arch:
        packages += ['tmux', 'lshw', 'ranger', 'dos2unix', 'bacula-client', 'vim-pathogen']
    elif targetsys == Systems.Fedora:
        packages += ['bacula-client', 'bacula-console-bat', 'bacula-traymonitor', 'dosemu']
    output('<green>Ok<nc>')
    install(installprog, packages)
    output('Programs installation...: <green>Done<nc>')

# Ubuntu: xaos, guake
def install_xprograms(targetsys, subsys, installprog, options):
    # [ ] cygwin                    [ ] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.1] Ubuntu
    # [ ] Fedora                    [ ] Mint
    output('Install X programs......: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.xprograms, options.noxprograms):
        output('<yellow>pass<nc>')
        return
    packages = ['xaos', 'guake', 'thunderbird', 'vlc', 'wmctrl', 'inkscape', 'audacity', 'gimp', 'bogofilter', 'hunspell', 'anki']
    if targetsys == Systems.BSD:
        packages += ['chromium', 'gnupg20', 'unetbootin', 'de-hunspell', 'ru-hunspell', 'fr-hunspell', 'es-hunspell']
    elif targetsys == Systems.Ubuntu:
        packages += ['vim-gtk', 'retext', 'chromium-browser', 'gpgv2', 'hunspell-de-de', 'hunspell-ru', 'hunspell-fr', 'hunspell-es']
    elif targetsys == Systems.SuSE:
        packages += ['chromium', 'gvim', 'retext', 'unetbootin']
    elif targetsys == Systems.Arch:
        packages += ['retext', 'chromium', 'mc', 'gvim', 'gnome-commander-git', 'file-commander-git']
    elif targetsys == Systems.Fedora:
        packages += ['gnome-commander', 'chromium', 'vim-X11', 'streamer1-plugins-base', 'gstreamer1-plugins-good',
                     'gstreamer1-plugins-ugly', 'gstreamer1-plugins-bad-free', 'gstreamer1-plugins-bad-free',
                     'gstreamer1-plugins-bad-freeworld', 'gstreamer1-plugins-bad-free-extras', 'ffmpeg', 'unetbootin',
                     'hunspell-de-de', 'hunspell-ru', 'hunspell-fr', 'hunspell-es']
    output('<green>Ok<nc>')
    install(installprog, packages)
    output('X Programs installation.: <green>Done<nc>')

def install_compiler(targetsys, subsys, installprog, options):
    # [ ] cygwin                    [ ] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.1] Ubuntu
    # [ ] Fedora                    [ ] Mint
    output('Install compiler........: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.compiler, options.nocompiler):
        output('<yellow>pass<nc>')
        return
    packages = ['meld', 'cgdb', 'gdb', 'cmake', 'ccache']
    if targetsys == Systems.BSD:
        packages += ['qt5', 'fsharp', 'mono', 'nodejs', 'yarn']
    elif targetsys == Systems.Ubuntu:
        packages += ['qt5-default', 'fsharp', 'mono-complete', 'nodejs', 'yarn']
    elif targetsys == Systems.SuSE:
        packages += ['fsharp', 'mono-complete', 'cmake-gui', 'kdevelop5', 'kdevelop5-pg-qt']
    elif targetsys == Systems.Arch:
        packages += ['qt5', 'mono', 'mono-tools', 'nodejs', 'yarn']
    elif targetsys == Systems.Fedora:
        packages += ['mono-complete', 'ncurses-devel', 'cmake-gui', 'nodejs', 'yarn']
    output('<green>Ok<nc>')
    install(installprog, packages)
    output('Compiler installation...: <green>Done<nc>')

def install_xfce_programs(targetsys, subsys, installprog, options):
    # [ ] cygwin                    [ ] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.1] Ubuntu
    # [ ] Fedora                    [ ] Mint
    output('Install XFCE programs...: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return
    if not options.desktop == 'xfce':
        output('<yellow>XFCE not used<nc>')
        return
    if not flag_is_set(options, options.xfce, options.noxfce):
        output('<yellow>pass<nc>')
        return
    # packages = ['']
    if targetsys == Systems.BSD or targetsys == Systems.Arch:
        packages = ['xfce4-xkb-plugin', 'xfce4-weather-plugin', 'xfce4-screenshooter-plugin', 'xfce4-cpugraph-plugin',
                     'xfce4-battery-plugin', 'xfce4-mailwatch-plugin']
    elif targetsys == Systems.Ubuntu:
        packages += ['xfce4-eyes-plugin']
    #elif targetsys == Systems.SuSE:
    #    packages += ['']
    #elif targetsys == Systems.Arch:
    #    packages += ['']
    #elif targetsys == Systems.Fedora:
    #    packages += ['']
    if not packages:
        output('<yellow>Pass<nc>')
    else:
        output('<green>Ok<nc>')
        install(installprog, packages)
        output('XFCE programs ..........: <green>Done<nc>')

def install_tex(targetsys, subsys, installprog, options):
    # [ ] cygwin                    [ ] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.1] Ubuntu
    # [ ] Fedora                    [ ] Mint
    output('Install TeX.............: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.tex, options.notex):
        output('<yellow>pass<nc>')
        return
    packages = ['texmaker', 'lyx', 'latex2html', 'texstudio']
    if targetsys == Systems.BSD:
        packages += ['latexila', 'texlive-full', 'font-cronyx-cyrillic', 'font-misc-cyrillic', 'font-screen-cyrillic',
                     'xorg-fonts-cyrillic']
    elif targetsys == Systems.Ubuntu:
        packages += ['latexila', 'texlive-music', 'xfonts-cyrillic', 'latex-cjk-japanese', 't1-cyrillic',
                     'texlive-lang-cyrillic', 'texlive-fonts-extra']
    elif targetsys == Systems.SuSE:
        packages += ['latexila', 'texlive-collection-music', 'texlive-cyrillic']
    elif targetsys == Systems.Arch:
        packages += ['texlive-music', 'texlive-langcyrillic', 'textlive-langjapanese']
    #elif targetsys == Systems.Fedora:
    #    packages += ['']
    output('<green>Ok<nc>')
    install(installprog, packages)
    output('TeX installation........: <green>Done<nc>')

def install_games(targetsys, subsys, installprog, options):
    # [ ] cygwin                    [ ] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.1] Ubuntu
    # [ ] Fedora                    [ ] Mint
    output('Install Games...........: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.games, options.nogames):
        output('<yellow>pass<nc>')
        return
    packages = ['xboard']
    if targetsys == Systems.BSD:
        packages += ['crafty', 'brutalchess', 'chessx', 'pouetchess']
    elif targetsys == Systems.Ubuntu:
        packages += ['phalanx', 'pychess', 'dosbox']
    elif targetsys == Systems.SuSE:
        packages += ['phalanx', 'gnome-chess', 'gnuchess', 'lskat kiten']
    elif targetsys == Systems.Arch:
        packages += ['pychess', 'chromium-bsu', 'dosbox']
    elif targetsys == Systems.Fedora:
        packages += ['dreamchess', 'gnuchess']
    output('<green>Ok<nc>')
    install(installprog, packages)
    output('Games installation......: <green>Done<nc>')

def install_fonts(targetsys, subsys, options):
    # [ ] cygwin                    [ ] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.1] Ubuntu
    # [ ] Fedora                    [ ] Mint
    output('Install Fonts...........: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.fonts, options.nofonts):
        output('<yellow>pass<nc>')
        return
    targetdir = '/usr/share/fonts' if not targetsys == Systems.BSD else '/usr/local/share/fonts/TTF'
    envyfonts = Path(targetdir).glob('Envy*.ttf')
    if envyfonts:
        output('<green>already installed<nc>')
    else:
        output('<tc>copying<nc>')
        fonts = Path(Basepath + '/data/font').glob('*.ttf')
        for font in fonts:
            subprocess.check_call(['sudo', 'cp', str(font), targetdir])
        #subprocess.check_call(['sudo', 'cp', '"' + Basepath + '/data/font/*"', targetdir])
        devnull = open(os.devnull, 'w')
        subprocess.check_call(['sudo', 'fc-cache', '-fv'], stdout=devnull)
        output('Fonts installed.........: <green>Done<nc>')

#region Cloning

def clone_from_github(src, project, flow):
    if os.path.isdir(src + project):
        return
    subprocess.check_call(['git', 'clone', 'git@github.com:slesa/' + project])
    if flow:
        os.system('cd '+project+" && git flow init -d && git checkout develop && cd ..")

def clone_github(root, options):
    output('Clone github ...........: ', False)
    if not flag_is_set(options, options.github, options.nogithub):
        output('<yellow>pass<nc>')
        return
    src = root + "/github/"
    if not os.path.isdir(src):
        os.mkdir(src)

    os.chdir(src)
    clone_from_github(src, 'Poseidon', True)
    clone_from_github(src, 'gui.cs', True)
    clone_from_github(src, 'sqlitestudio', True)
    clone_from_github(src, 'Trinity', True)
    clone_from_github(src, 'Godot', False)
    os.chdir('..')

    output('Clone github............: <green>Done<nc>')

def clone_from_gitlab(src, project, flow):
    if os.path.isdir(src + project):
        return
    subprocess.check_call(['git', 'clone', 'git@gitlab.com:slesa/' + project])
    if flow:
        os.system('cd '+project+" && git flow init -d && git checkout develop && cd ..")

def clone_gitlab(root, options):
    output('Clone gitlab ...........: ', False)
    if not flag_is_set(options, options.gitlab, options.nogitlab):
        output('<yellow>pass<nc>')
        return
    src = root + "/gitlab/"
    if not os.path.isdir(src):
        os.mkdir(src)

    os.chdir(src)
    clone_from_gitlab(src, 'waiterwatch', True)
    clone_from_gitlab(src, 'aikidoka', True)
    clone_from_gitlab(src, 'monty', False)
    os.chdir('..')

    output('Clone gitlab............: <green>Done<nc>')

def clone_all(options):
    output('Cloning sources.........: ', False)
    if not flag_is_set(options, options.clone, options.noclone):
        output('<yellow>pass<nc>')
        return
    src = str(Path.home()) + '/work'
    if not os.path.isdir(src):
        os.mkdir(src)
    clone_github(src, options)
    clone_gitlab(src, options)

#endregion Cloning

def install_qt(targetsys, options, downloads, work):
    output('install Qt .............: ', False)
    if options.qt and (not options.full or options.noqt):
        output('<yellow>pass<nc>')
        return

    if os.path.isdir(work+'/Qt') or os.path.isdir(work+'/qt'):
        output('<yellow>already installed<nc>')
        return
    path = os.getcwd()
    os.chdir(downloads)

    qtinstaller = 'qt-unified-linux-x64-online.run' 
    if targetsys==Systems.Cygwin:
        qtinstaller = 'qt-unified-windows-x86-online.exe'
    elif targetsys==Systems.MacOS:
        qtinstaller = 'qt-unified-mac-x64-online.dmg'
    if not os.path.isfile(qtinstaller):
        subprocess.check_call(['wget', 'https://download.qt.io/official_releases/online_installers/'+qtinstaller])
        subprocess.check_call(['chmod', '+x', qtinstaller])
    #copy_text_to_clipboard(targetsys, work+'/qt')
    subprocess.check_call(['./'+qtinstaller])

    os.chdir(path)
    output('Qt installed ...........: <green>Done<nc>')

def install_rider(targetsys, options, downloads, bin):
    output('install Rider...........: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if options.rider and (not options.full or options.norider):
        output('<yellow>pass<nc>')
        return

    riderdir = bin + '/Jetbrains.Rider'
    if os.path.isdir(riderdir):
        output('<yellow>already installed<nc>')
        return
    path = os.getcwd()
    os.chdir(downloads)
    riderzip = 'JetBrains.Rider-2019.2.3.tar.gz'
    if not os.path.isfile(riderzip):
        subprocess.check_call(['wget', 'https://download.jetbrains.com/rider/'+riderzip])
    os.chdir(bin)
    subprocess.check_call(['tar', 'xvzf', downloads+'/'+riderzip])
    subprocess.check_call(['mv', 'JetBrains\ Rider*', riderdir])

    os.chdir(path)
    output('Rider installed ........: <green>Done<nc>')

def install_pycharm(targetsys, options, downloads, bin):
    output('install PyCharm.........: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if options.pycharm and (not options.full or options.nopycharm):
        output('<yellow>pass<nc>')
        return

    charmdir = bin + '/Jetbrains.PyCharm'
    if os.path.isdir(charmdir):
        output('<yellow>already installed<nc>')
        return
    path = os.getcwd()
    os.chdir(downloads)
    charmzip = 'pycharm-community-2019.2.4.tar.gz'
    if not os.path.isfile(charmzip):
        subprocess.check_call(['wget', 'https://download.jetbrains.com/python/'+charmzip])
    os.chdir(bin)
    subprocess.check_call(['tar', 'xvzf', downloads+'/'+charmzip])
    subprocess.check_call(['mv', 'pycharm-community*', charmdir])

    os.chdir(path)
    output('PyCharm installed.......: <green>Done<nc>')

def install_externals(targetsys, subsys, options):
    # [ ] cygwin                    [ ] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.1] Ubuntu
    # [ ] Fedora                    [ ] Mint
    output('Install externals.......: ', False)
    #if not options.externals or (options.full and options.noexternals):
    if subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return
    if options.noexternals:
        output('<yellow>pass<nc>')
        return
    downloads = str(Path.home()) + '/Downloads'
    if not os.path.isdir(downloads):
        os.mkdir(downloads)
    work = str(Path.home()) + '/work'
    bin = str(Path.home()) + '/bin'

    install_qt(targetsys, options, downloads, work)
    install_rider(targetsys, options, downloads, bin)
    install_pycharm(targetsys, options, downloads, bin)

    output('Externals installed.....: <green>Done<nc>')


def install_all(targetsys, subsys, installprog, options):
    # [ ] cygwin                    [ ] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.1] Ubuntu
    # [ ] Fedora                    [ ] Mint
    install_core(targetsys, subsys, installprog, options)
    install_dotfiles(options)
    install_zsh(targetsys, options)
    install_login(targetsys, subsys, options)
    install_links(targetsys, subsys, options)
    install_owncube(targetsys, subsys, installprog, options)
    clone_all(options)
    # create_ssh_key
    install_basics(targetsys, subsys, installprog, options)
    install_programs(targetsys, subsys, installprog, options)
    install_xprograms(targetsys, subsys, installprog, options)
    install_compiler(targetsys, subsys, installprog, options)
    install_xfce_programs(targetsys, subsys, installprog, options)
    install_tex(targetsys, subsys, installprog, options)
    install_games(targetsys, subsys, installprog, options)
    install_fonts(targetsys, subsys, options)
    install_externals(targetsys, subsys, options)


output("<head>=====[ Configuring system ]====<nc>")
(system,subsys) = determine_os()
installer = determine_installer(system)
args = create_parser()

#output(f'Systems is <green>{system}<nc> with installer <tc>{installer}<nc>')
#copy_text_to_clipboard(system, 'This is a test clip')
#ensure_root(system)
install_all(system, subsys, installer, args)


#installXfceLinks # no arg
##installTwitter
#installExternals