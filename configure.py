# 0.B - Fedora
# 0.A - MX
# 0.9 - FreeBSD
# 0.8 - Manjaro
# 0.7 - Zorin
# 0.6 - Fedora
# 0.5 - Xubuntu
# 0.4 - Ubuntu
# 0.3 - Cygwin
# 0.2 - Ubuntu on Windows
import os
import shutil
import glob
import platform
import subprocess
from pathlib import Path
from enum import Enum

# Renoise, mp3 (-verwaltung), GitKraken?, XMind

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
    parser.add_argument('--desktop', default='xfce', choices=['xfce', 'kde', 'gnome'])
    parser.add_argument('--full', action='store_true')
    parser.add_argument('--zsh', action='store_true')
    parser.add_argument('--nozsh', action='store_true')
    parser.add_argument('--prezto', action='store_true')
    parser.add_argument('--noprezto', action='store_true')
    parser.add_argument('--login', action='store_true')
    parser.add_argument('--nologin', action='store_true')
    parser.add_argument('--links', action='store_true')
    parser.add_argument('--nolinks', action='store_true')
    parser.add_argument('--core', action='store_true')
    parser.add_argument('--nocore', action='store_true')
    parser.add_argument('--nextcloud', action='store_true')
    parser.add_argument('--nonextcloud', action='store_true')
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
    parser.add_argument('--gf', action='store_true')
    parser.add_argument('--nogf', action='store_true')
    parser.add_argument('--externals', action='store_true')
    parser.add_argument('--noexternals', action='store_true')
    parser.add_argument('--qt', action='store_true')
    parser.add_argument('--noqt', action='store_true')
    parser.add_argument('--rider', action='store_true')
    parser.add_argument('--norider', action='store_true')
    parser.add_argument('--pycharm', action='store_true')
    parser.add_argument('--nopycharm', action='store_true')
    parser.add_argument('--clion', action='store_true')
    parser.add_argument('--noclion', action='store_true')
    parser.add_argument('--storm', action='store_true')
    parser.add_argument('--nostorm', action='store_true')
    parser.add_argument('--code', action='store_true')
    parser.add_argument('--nocode', action='store_true')
    parser.add_argument('--dotnet', action='store_true')
    parser.add_argument('--nodotnet', action='store_true')
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
  Zorin = 8
  MxLinux = 9
class Subsys(Enum):
  Origin = 0
  Windows = 1

def determine_os():
    output(f'System..................: <green>{platform.system()}<nc>')
    # [0.3] cygwin                  [0.A] Debian
    # [ ] macos                     [ ] SuSE
    # [0.9] FreeBSD                 [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.5] Ubuntu
    # [ ] Fedora                    [0.7] Zorin
    
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
        linux = platform.platform().lower() + platform.version().lower()
        if '.fc3' in linux:
            output('<green>Fedora<nc>')
            return (Systems.Fedora,subsys)
        if 'mx' in linux:
            output('<green>MXLinux<nc>')
            return (Systems.MxLinux,subsys)
        if 'suse' in linux:
            output('<green>SuSE<nc>')
            return (Systems.SuSE,subsys)
        if 'arch' in linux or 'manjaro' in linux:
            output('<green>Arch / Manjaro<nc>')
            return (Systems.Arch,subsys)
        if 'ubuntu' in linux:
            output(f'<green>Ubuntu {subsys}<nc>')
            return (Systems.Ubuntu,subsys)
        if 'zorin' in linux:
            output(f'<green>Zorin {subsys}<nc>')
            return (Systems.Zorin,subsys)
    output('<red>Unknown<nc>')
    output(f'Platform................: <yellow>{platform.platform()}<nc>')
    output(f'Release.................: <yellow>{platform.release()}<nc>')
    output(f'Version.................: <yellow>{platform.version()}<nc>')
    #output(f'Uname...................: <yellow>{str(platform.uname())}<nc>')
    #output(f'Distribution............: <yellow>{platform.linux_distribution()[0]}<nc>')
    return (None,subsys)

def determine_installer(os):
    if os == Systems.BSD:
        return ["sudo", "pkg", "install", "-y"]
    if os == Systems.Fedora:
        return ["sudo", "dnf", "install", "-y"]
    if os == Systems.MxLinux:
        return ["sudo", "apt-get", "install", "-y"]
    if os == Systems.SuSE:
        return ["sudo", "zypper", "install", "-ly"]
    if os == Systems.Arch:
        return ["sudo", "pacman", "--noconfirm", "-Syu"]
    if os == Systems.Ubuntu or os == Systems.Zorin:
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

def get_downloads():
    downloads = str(Path.home()) + '/Downloads'
    if not os.path.isdir(downloads):
        os.mkdir(downloads)
    return downloads

#endregion

def install_dotfiles(options):
    # [0.3] cygwin                  [0.B] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.5] Ubuntu
    # [ ] Fedora                    [0.7] Zorin
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

def install_zsh(targetsys, options):
    # [0.3] cygwin                  [0.B] Fedora
    # [ ] macos                     [ ] SuSE
    # [0.9] FreeBSD                 [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.5] Ubuntu
    # [0.A] MX                      [0.7] Zorin
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
        elif targetsys == Systems.Ubuntu or targetsys == Systems.Zorin:
            srcfile = 'zshrc.ubuntu'
        else:
            srcfile = 'zshrc.ubuntu'
        subprocess.check_call(['cp', Basepath + '/data/templ/' + srcfile, targetfile])
        output('zshrc installed.........: <green>Done<nc>')
    if targetsys != Systems.Cygwin:
        output('set zsh shell...........: ', False)
        currentshell = os.popen('echo $SHELL').read()
        if 'zsh' in currentshell:
            output('<yellow>already set<nc>')
        else:
            shell = os.popen('which zsh').read()[:-1]
            subprocess.check_call(['chsh', '-s', shell])
    output('<green>Done<nc>')

def install_prezto(targetsys, options):
    # [ ] cygwin                    [0.B] Fedora
    # [ ] macos                     [ ] SuSE
    # [0.9] FreeBSD                 [ ] Arch / Manjaro
    # [ ] Ubuntu on Windows         [0.5] Ubuntu
    # [0.A] MX                      [0.7] Zorin
    output('Install Prezto..........: ', False)
    if not flag_is_set(options, options.prezto, options.noprezto):
        output('<yellow>pass<nc>')
        return
    path = str(Path.home()) + '/.zprezto'
    if os.path.isdir(path):
        output('<yellow>already there<nc>')
        return
    subprocess.check_call(['git', 'clone', '--recursive', 'https://github.com/sorin-ionescu/prezto.git', path])
    subprocess.check_call(['echo', '"~/.zprezto/init.zsh"', '>>', '~/.zshrc'])
    output('<green>Done<nc>')

#    cmd = """setopt EXTENDED_GLOB; 
#            for rcfile in ~/.zprezto/runcoms/^README.md(.N); do
#             ln -s $rcfile ~/.zprezto/.${rcfile:t}
#             done"""
#    os.popen(cmd)


def install_login(targetsys, subsys, options):
    # [0.3] cygwin                  [0.B] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.5] Ubuntu
    # [0.A] MX                      [0.7] Zorin
    output('Install Login...........: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.login, options.nologin):
        output('<yellow>pass<nc>')
        return
    targetdir = '/usr/share/backgrounds/'
    targetfile = 'StarTrekLogo1920x1080.jpg'
    configfile = '/etc/lightdm/lightdm-gtk-greeter.conf'
    if targetsys == Systems.SuSE:
        targetdir = '/usr/share/wallpapers/'
    #elif targetsys == Systems.Fedora or targetsys == Systems.MxLinux:
    #    targetdir = '/usr/share/backgrounds/'
    elif targetsys == Systems.BSD:
        targetdir = '/usr/local/share/backgrounds/'
        configfile = '/usr/local/share/PCDM/themes/trueos/trueos.theme'
    if not os.path.isfile(targetdir + targetfile):
        subprocess.check_call(['sudo', 'cp', Basepath + '/data/img/' + targetfile, targetdir + targetfile])
        subprocess.check_call(['sudo', 'chmod', '+r', targetdir + targetfile])
    if options.desktop=='xfce':
        r1 = subprocess.run(['sudo', 'sed', '-i', '-e', f's#^background=.*#background={targetdir}{targetfile}#g', configfile ])
        #print(r1)
        r2 = subprocess.run(['sudo', 'sed', '-i', '-e', 's/\#theme-name=/theme-name=Ambience/g', configfile ])
        #print(r2)
 
    output('<green>Ok<nc>')

def install_fonts(targetsys, subsys, options):
    # [0.3] cygwin                  [0.B] Fedora
    # [ ] macos                     [ ] SuSE
    # [0.9] FreeBSD                 [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.5] Ubuntu
    # [0.A] MX                      [0.7] Zorin
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

#region File links

def link_file(source, target):
    if not os.path.islink(target):
        os.symlink(source, target)

def link_unix_file(filename, folder=''):
    source = Basepath + '/etc/unix/'
    if folder:
        source = source + folder + '/'
    target = '/.' + filename if not '/' in filename else '/.config/' + filename
    target = str(Path.home()) + target

    targetdir = os.path.dirname(target)
    if not os.path.isdir(targetdir):
        os.mkdir(targetdir)

    link_file(source + filename, target)

def link_autostart(filename):
    target = str(Path.home()) + '/.config/autostart/' + filename
    if not os.path.islink(target):
        source = Basepath + '/etc/unix/autostart/' + filename
        os.symlink(source, target)

def link_xfce_file(filename, folder=''):
    source = Basepath + '/etc/unix/xfce4/' + filename
    target = str(Path.home()) + '/.config/xfce4/'
    if folder:
        target = target + folder + '/'
    target += filename

    if os.path.islink(target):
        return
    if os.path.isfile(target):
        os.rename(target, target + '.bak')
    os.symlink(source, target)

def copy_xfce_launcher(filename, id):
    source = Basepath + '/etc/unix/xfce4/' + filename
    target = str(Path.home()) + '/.config/xfce4/panel/launcher-' + str(id)
    if not os.path.isdir(target):
        os.mkdir(target)
    target += '/' + filename
    if os.path.islink(target):
        return
    shutil.copy(source, target)

def clear_xfce_launchers():
    targets = str(Path.home()) + '/.config/xfce4/panel/launcher-*'
    launchers = glob.glob(targets)
    for launcher in launchers:
        shutil.rmtree(launcher)


def install_links(targetsys, subsys, options):
    # [0.3] cygwin                  [0.B] Fedora
    # [ ] macos                     [ ] SuSE
    # [0.9] FreeBSD                 [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.5] Ubuntu
    # [0.A] MX                      [0.7] Zorin
    output('Install Links...........: ', False)
    if not flag_is_set(options, options.links, options.nolinks):
        output('<yellow>pass<nc>')
        return
    bindir = str(Path.home()) + '/bin'
    if not os.path.isdir(bindir):
        os.mkdir(bindir)
    if not os.path.islink(bindir+'/tools'):
        os.symlink(Basepath + '/bin/tools', bindir+'/tools')

    link_unix_file('zsh')
    link_unix_file('tmux.conf')
    link_unix_file('gitconfig')
    link_unix_file('vimrc')

    link_unix_file('devilspie2/window_open.lua')

    link_unix_file('zprofile', 'zprezto')
    link_unix_file('zlogin', 'zprezto')
    link_unix_file('zlogout', 'zprezto')
    link_unix_file('zpreztorc', 'zprezto')
    link_unix_file('zshenv', 'zprezto')
    link_unix_file('p10k.zsh', 'zprezto')

    # Autostart
    if not targetsys==Systems.Cygwin and not subsys == Subsys.Windows:
        autosource = Basepath + '/etc/unix/autostart/'
        autostart = str(Path.home()) + '/.config/autostart/'
        if not os.path.isdir(autostart):
            os.mkdir(autostart)
        link_autostart('nextCloud.desktop')
        link_autostart('Thunderbird.desktop')
        # link_autostart('Twitter.desktop')
        link_autostart('Pidgin.desktop')
        link_autostart('devilspie.desktop')

    # Xfce
    xfceSource = Basepath + '/etc/unix/xfce4/'
    xfcePath = str(Path.home()) + '/.config/xfce4/'
    xfcePanel = 'panel/'
    # xfceChannel = 'xfconf/xfce-perchannel-xml/'
    if not targetsys==Systems.Cygwin and not subsys == Subsys.Windows:
        link_xfce_file('xfce4-orageclock-plugin-17.rc', xfcePanel)
        link_xfce_file('weather-8.rc', xfcePanel)
        link_xfce_file('eyes-6.rc', xfcePanel)
        link_xfce_file('cpugraph-11.rc', xfcePanel)
        link_xfce_file('netload-12.rc', xfcePanel)
        clear_xfce_launchers()
        copy_xfce_launcher('exo-terminal-emulator.desktop', 19)
        copy_xfce_launcher('exo-terminal-byobu.desktop', 20)
        copy_xfce_launcher('exo-file-manager.desktop', 21)
        copy_xfce_launcher('exo-file-commander.desktop', 22)
        copy_xfce_launcher('exo-firefox.desktop', 23)
        copy_xfce_launcher('exo-chromium.desktop', 24)
        
    output('<green>Ok<nc>')

#endregion


# todo:    subprocess.check_call(['git', 'clone', 'git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim', path])

#region Collect packages

def install_core(installprog, targetsys, subsys, options):
    # [0.3] cygwin                  [0.B] Fedora
    # [ ] macos                     [ ] SuSE
    # [0.9] FreeBSD                 [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.5] Ubuntu
    # [0.A] MX                      [0.7] Zorin
    output('Collect core............: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.core, options.nocore):
        output('<yellow>pass<nc>')
        return
    packages = ['vim', 'zsh']
    if subsys == Subsys.Origin: # Not needed on Win Subsys
        packages += ['git', 'firefox']
    if targetsys == Systems.BSD:
        packages += ['gitflow', 'pidof', 'links', 'wget', 'bsdstats', 'linux_base-c7', 'portmaster']
    else:
        packages += ['xsel']
    install(installprog, packages)
    output('<green>Ok<nc>')

def install_nextcloud(targetsys, subsys, options):
    # [0.3] cygwin                  [0.B] Fedora
    # [ ] macos                     [ ] SuSE
    # [0.9] FreeBSD                 [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.5] Ubuntu
    # [0.A] MX                      [0.7] Zorin
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
    #if not get_pid('nextcloud'):
    #    subprocess.Popen('nextcloud')

def install_basics(targetsys, subsys, options):
    # [0.3] cygwin                  [0.B] Fedora
    # [ ] macos                     [ ] SuSE
    # [0.9] FreeBSD                 [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.5] Ubuntu
    # [0.A] MX                      [0.7] Zorin
    output('Collect basics..........: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return []
    if not flag_is_set(options, options.basics, options.nobasics):
        output('<yellow>pass<nc>')
        return []
    packages = ['zsh']
    if targetsys == Systems.BSD:
        packages += ['gitflow', 'fortune-mod-bofh', 'pstree', 'hexchat', 'synergy']
    elif targetsys == Systems.MxLinux:
        packages += ['git-flow', 'fortunes', 'fortunes-de']
    elif targetsys == Systems.Ubuntu or targetsys == Systems.Zorin:
        packages += ['git-flow', 'fortunes', 'fortunes-de']
        if subsys==Subsys.Origin:
          packages += ['hfsplus', 'hfsutils', 'synergy', 'rdesktop']
    elif targetsys == Systems.SuSE:
        packages += ['git-flow', 'fortune', 'hfsutils', 'synergy', 'qsynergy', 'rdesktop', 'gcc-c++', 'gcc']
    elif targetsys == Systems.Arch:
        packages += ['synergy', 'fortune-mod', 'zsh-lovers']
    elif targetsys == Systems.Fedora: # gitflow
        packages += ['fortune-mod', 'hfsutils', 'zsh-lovers', 'rdesktop', 'gcc-c++', 'synergy']
    output('<green>Ok<nc>')
    return packages

# Ubuntu: tmuxinator, tmux-plugin-manager ranger
def install_programs(targetsys, subsys, options):
    # [0.3] cygwin                  [0.B] Fedora
    # [ ] macos                     [ ] SuSE
    # [0.9] FreeBSD                 [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.5] Ubuntu
    # [0.A] MX                      [0.7] Zorin
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
        packages += ['postgresql12-server', 'postgresql12-client', 'tmux', 'bacula9-client', 'xorg']
    elif targetsys == Systems.MxLinux:
        packages += ['postgresql-11','tmux','ranger','dos2unix','openssh-server','vim-addon-manager', 'vim-pathogen','bacula-client']
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
            packages += ['postgresql-server', 'postgresql-contrib', 'tmux', 'bacula-client', 'bacula-console-bat', 'bacula-traymonitor'] #, 'dosemu']
    output('<green>Ok<nc>')
    return packages

# Ubuntu: xaos, guake
def install_xprograms(targetsys, subsys, options):
    # [0.3] cygwin                  [0.B] Fedora
    # [ ] macos                     [ ] SuSE
    # [0.9] FreeBSD                 [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.5] Ubuntu
    # [0.A] MX                      [0.7] Zorin
    output('Collect X programs......: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return []
    if not flag_is_set(options, options.xprograms, options.noxprograms):
        output('<yellow>pass<nc>')
        return []
    packages = ['xaos', 'thunderbird', 'wmctrl', 'inkscape', 'audacity', 'gimp', 'bogofilter', 'hunspell', 'anki', 'devilspie2', 'cawbird', 'pidgin']
    if targetsys == Systems.BSD:
        packages += ['chromium', 'vlc', 'gnupg', 'unetbootin', 'de-hunspell', 'ru-hunspell', 'fr-hunspell', 'es-hunspell']
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
        packages += [ 'gnome-commander', 'retext', 'chromium', 'vim-X11', 'gstreamer1-plugins-good',
                     'gstreamer1-plugins-bad-free', 'gstreamer1-plugins-bad-free',
                     'gstreamer1-plugins-bad-free-extras', 'unetbootin',
                     'hunspell-de', 'hunspell-ru', 'hunspell-fr', 'hunspell-es']
                     #['streamer1-plugins-base', 'gstreamer1-plugins-ugly','gstreamer1-plugins-bad-freeworld','ffmpeg',   ]
    output('<green>Ok<nc>')
    return packages

def install_compiler(targetsys, subsys, options):
    # [0.3] cygwin                  [0.B] Fedora
    # [ ] macos                     [ ] SuSE
    # [0.9] FreeBSD                 [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.5] Ubuntu
    # [0.A] MX                      [0.7] Zorin
    output('Install compiler........: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return []
    if not flag_is_set(options, options.compiler, options.nocompiler):
        output('<yellow>pass<nc>')
        return []
    packages = ['meld', 'cgdb', 'gdb', 'cmake', 'ccache']
    if targetsys == Systems.BSD:
        packages += ['qt5','qt5-designer', 'qtcreator']
        #packages += ['qt5-core', 'qt5-3d', 'qt5-gui', 'qt5-serialbus', 'qt5-widgets', 'qt5-xml', 'qt5-xmlpatterns', 'qt5-qtpaths', 'qt5-charts', 'qt5-connectivity']
        #packages += ['qt5-examples', 'qt5-sensors', 'qt5-serialport', 'qt5-speech', 'qt5-sql', 'qt5-sqldrivers-sqlite3', 'qt5-sqldrivers-pgsql', 'qt5-x11extras']
        #packages += ['qt5-style-qtcurve', 'qt5-svg', 'qt5-uiplugin', 'qt5-wayland', 'qt5-webchannel', 'qt5-webglplugin', 'qt5-webkit', 'qt5-websockets', 'qt5-testlib']
        #packages += ['qt5-webview', 'qt5-widgets', 'qt5-scxml', 'qt5-printsupport', 'qt5-qdoc', 'qt5-qdbus', 'qt5-network', 'qt5-opengl', 'qt5-imageformats', 'qt5-buildtools']
        packages += ['fsharp', 'mono', 'node-14.4.0', 'npm', 'yarn', 'openjdk14']
    elif targetsys == Systems.Ubuntu or targetsys == Systems.Zorin:
        packages += ['qt5-default', 'fsharp', 'mono-complete', 'nodejs', 'yarn']
    elif targetsys == Systems.SuSE:
        packages += ['fsharp', 'mono-complete', 'cmake-gui', 'kdevelop5', 'kdevelop5-pg-qt']
    elif targetsys == Systems.Arch:
        packages += ['qt5', 'mono', 'mono-tools', 'nodejs', 'yarn']
    elif targetsys == Systems.Fedora:
        packages += ['mono-complete', 'ncurses-devel', 'cmake-gui', 'nodejs', 'mesa-libGL', 'mesa-libGL-devel'] #, 'yarn']
    elif targetsys == Systems.MxLinux:
        packages += ['python3-venv','mono-complete','cmake-qt-gui','yarnpkg','pyqt5-dev','pyqt5-examples','qt5-default','qtbase5-dev','libgl1-mesa-dev','libglu1-mesa-dev']
    output('<green>Ok<nc>')
    return packages

def install_dotnet(installprog, targetsys, options):
    # [0.3] cygwin                  [0.B] Fedora
    # [ ] macos                     [ ] SuSE
    # [0.9] FreeBSD                 [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.5] Ubuntu
    # [0.A] MX                      [0.7] Zorin
    output('install .NET Core ......: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.dotnet, options.nodotnet):
        output('<yellow>pass<nc>')
        return
    path = os.getcwd()
    os.chdir('/tmp')

    packages = ['dotnet-sdk-5.0', 'aspnetcore-runtime-5.0', 'dotnet-sdk-3.1', 'aspnetcore-runtime-3.1', 'dotnet-runtime-3.1']
    packages = ['dotnet-sdk-3.1', 'aspnetcore-runtime-3.1', 'dotnet-runtime-3.1']

    if targetsys == Systems.BSD:
        packages = ['linux-dotnet10-sdk', 'linux-dotnet10-runtime']
    elif targetsys == Systems.Ubuntu or targetsys == Systems.Zorin or targetsys == Systems.MxLinux:
        os.popen('wget https://packages.microsoft.com/config/ubuntu/20.10/packages-microsoft-prod.deb -O packages-microsoft-prod.deb')
        os.popen('sudo dpkg -i packages-microsoft-prod.deb')
    elif targetsys == Systems.SuSE:
        os.popen('sudo zypper install libicu')
        os.popen('sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc')
        os.popen('wget https://packages.microsoft.com/config/opensuse/15/prod.repo')
        os.popen('sudo mv prod.repo /etc/zypp/repos.d/microsoft-prod.repo')
        os.popen('sudo chown root:root /etc/zypp/repos.d/microsoft-prod.repo')
    elif targetsys == Systems.Arch:
        output('<red>unsupported<nc>')
    elif targetsys == Systems.Fedora:
        os.popen('sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc')
        os.popen('sudo wget -O /etc/yum.repos.d/microsoft-prod.repo https://packages.microsoft.com/config/fedora/33/prod.repo')
        os.popen('sudo dnf check-update')
    os.chdir(path)

    install(installprog, packages)
    output('<green>Ok<nc>')

def install_xfce_programs(targetsys, subsys, options):
    # [0.3] cygwin                  [0.B] Fedora
    # [ ] macos                     [ ] SuSE
    # [0.9] FreeBSD                 [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.5] Ubuntu
    # [0.A] MX                      [0.7] Zorin
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
    packages = []
    if targetsys == Systems.BSD or targetsys == Systems.Arch:
        packages = ['xfce4-xkb-plugin', 'xfce4-weather-plugin', 'xfce4-screenshooter-plugin', 'xfce4-cpugraph-plugin',
                     'xfce4-battery-plugin', 'xfce4-mailwatch-plugin']
    elif targetsys == Systems.Ubuntu or targetsys == Systems.Zorin or targetsys == Systems.Fedora or targetsys == Systems.MxLinux:
        packages = ['xfce4-eyes-plugin']
    #elif targetsys == Systems.SuSE:
    #    packages += ['']
    #elif targetsys == Systems.Arch:
    #    packages += ['']
    #elif targetsys == Systems.Fedora:
    #    packages += ['']
    output('<green>Ok<nc>')
    return packages

def install_tex(targetsys, subsys, options):
    # [0.3] cygwin                  [0.B] Fedora
    # [ ] macos                     [ ] SuSE
    # [0.9] FreeBSD                 [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.5] Ubuntu
    # [0.A] MX                      [0.7] Zorin
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
        packages += ['texlive-music', 'texlive-langcyrillic', 'textlive-langjapanese']
    #elif targetsys == Systems.Fedora:
    #    packages += ['']
    output('<green>Ok<nc>')
    return packages

def install_games(targetsys, subsys, options):
    # [0.3] cygwin                  [0.B] Fedora
    # [ ] macos                     [ ] SuSE
    # [0.9] FreeBSD                 [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.5] Ubuntu
    # [0.A] MX                      [0.7] Zorin
    output('Collect Games...........: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return []
    if not flag_is_set(options, options.games, options.nogames):
        output('<yellow>pass<nc>')
        return []
    packages = ['xboard']
    if targetsys == Systems.BSD:
        packages += ['crafty', 'brutalchess', 'chessx', 'pouetchess']
    elif targetsys == Systems.MxLinux:
        packages += ['phalanx','pychess','dosbox','xskat','crafty','glhack','slashem','quake','quake2']
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

#endregion

#region Cloning

def install_gitflow():
    output('Installing git flow ....: ', False)

    flow = os.popen('which git-flow').read()[:-1]
    if "/git-flow" in flow:
        output('<yellow>Already installed<nc>')
        return

    path = os.getcwd()
    os.chdir(get_downloads())

    subprocess.check_call(['curl', '-OL', 'https://raw.github.com/nvie/gitflow/develop/contrib/gitflow-installer.sh'])
    subprocess.check_call(['chmod', '+x', 'gitflow-installer.sh'])
    subprocess.check_call(['sudo', './gitflow-installer.sh'])

    os.chdir(path)
    output('<green>Done<nc>')

#region Github

def clone_from_github(src, project, flow, base=''):
    if os.path.isdir(src + project):
        return
    header = 'git@' if '/' not in project else 'https://'
    target = ':slesa/'+project if '/' not in project else '/'+project
    subprocess.check_call(['git', 'clone', header + 'github.com' + target])
    if base:
        os.system('cd '+project+f" && git remote add upstream {base} && cd ..")
    if flow:
        os.system('cd '+project+" && git flow init -d && git checkout develop && cd ..")

def clone_safe_from_github(root):
    src = root + "/github/safe/"
    if not os.path.isdir(src):
        os.mkdir(src)

    os.chdir(src)
    clone_from_github(src, 'Terminal.Gui.Elmish', True, 'https://github.com/DieselMeister/Terminal.Gui.Elmish.git')
    clone_from_github(src, 'SAFE-Nightwatch', True, 'https://github.com/SAFE-Stack/SAFE-Nightwatch.git')
    clone_from_github(src, 'SAFE-BookStore', True, 'https://github.com/SAFE-Stack/SAFE-BookStore.git')
    clone_from_github(src, 'ConfPlanner', True, 'https://github.com/SAFE-Stack/SAFE-ConfPlanner.git')
    clone_from_github(src, 'gui.cs', True, 'https://github.com/migueldeicaza/gui.cs.git')
    clone_from_github(src, 'LibAAS', True, 'https://github.com/mastoj/LibAAS.git')
    os.chdir('..')
    os.chdir('..')

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
    clone_from_github(src, 'FsReveal', False)
#    clone_from_github(src, 'odoo/odoo', False)

    clone_from_github(src, 'FAKE', True, 'https://github.com/fsharp/FAKE.git')
    clone_from_github(src, 'machine.specifications', True, 'https://github.com/machine/machine.specifications.git')
    clone_from_github(src, 'EventStore', True, 'https://github.com/EventStore/EventStore.git')

    os.chdir('..')
    clone_safe_from_github(root)
    output('<green>Done<nc>')

#endregion

#region Gitlab

def clone_from_xfce(src, ns, project):
    if os.path.isdir(src + project):
        return
    link = "git@gitlab.xfce.org:"
    subprocess.check_call(['git', 'clone', link + ns + '/' + project])

def clone_xfce_from_gitlab(root):
    src = root + "/xfce/"
    if not os.path.isdir(src):
        os.mkdir(src)

    os.chdir(src)
    clone_from_xfce(src, 'xfce', 'xfce4-dev-tools')
    clone_from_xfce(src, 'xfce', 'libxfce4ui')
    clone_from_xfce(src, 'xfce', 'xfce4-panel')
    clone_from_xfce(src, 'xfce', 'xfce4-settings')
    clone_from_xfce(src, 'apps', 'xfce4-panel-profiles')
    clone_from_xfce(src, 'panel-plugins', 'xfce4-sample-plugin')
    clone_from_xfce(src, 'panel-plugins', 'xfce4-smartbookmark-plugin')
    os.chdir('..')

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
    clone_from_gitlab(src, 'ravebase', False)
    os.chdir('..')
    clone_xfce_from_gitlab(root)

    output('<green>Done<nc>')

#endregion

#region 42 repos

def clone_from_gf(src, sub, project, flow):
    
    if os.path.isdir(src + project):
        return
    subprocess.check_call(['git', 'clone', 'https://develop.42gmbh.com/bitbucket/scm/'+sub+'/'+project+'.git'])
    if flow:
        os.system('cd '+project+" && git flow init -d && cd ..")

def clone_gf(root, options):
    output('Clone 42................: ', False)
    if not flag_is_set(options, options.gf, options.nogf):
        output('<yellow>pass<nc>')
        return
    src = root + "/42/"
    if not os.path.isdir(src):
        os.mkdir(src)

    os.chdir(src)
    clone_from_gf(src, 'macl', 'matrixclassic', True)
    clone_from_gf(src, 'bv', 'bonviewer', True)
    clone_from_gf(src, 'mat', 'matrixodooaddons', False)
    clone_from_gf(src, 'mat', 'matrixbackoffice', False)
    clone_from_gf(src, 'mat', 'tseconnector', False)
    clone_from_gf(src, 'bv', 'playground', False)
    os.chdir('..')

    output('<green>Done<nc>')

#endregion

def clone_all(options):
    output('Cloning sources.........: ', False)
    if not flag_is_set(options, options.clone, options.noclone):
        output('<yellow>pass<nc>')
        return
    output('')
    src = str(Path.home()) + '/work'
    if not os.path.isdir(src):
        os.mkdir(src)
    clone_github(src, options)
    clone_gitlab(src, options)
    clone_gf(src, options)

    output('<green>Done<nc>')


#endregion Cloning

#region External programs

def install_qt(targetsys, options, downloads, work):
    output('- install Qt ...........: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.qt, options.noqt):
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
    subprocess.Popen(['./'+qtinstaller])

    os.chdir(path)
    output('- Qt installed .........: <green>Done<nc>')

def install_rider(targetsys, options, downloads, bin):
    output('- install Rider.........: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.rider, options.norider):
        output('<yellow>pass<nc>')
        return

    riderdir = bin + '/Jetbrains.Rider'
    if os.path.isdir(riderdir):
        output('<yellow>already installed<nc>')
        return
    path = os.getcwd()
    os.chdir(downloads)
    riderzip = 'JetBrains.Rider-2020.3.2.tar.gz'
    if not os.path.isfile(riderzip):
        subprocess.check_call(['wget', 'https://download.jetbrains.com/rider/'+riderzip])
    os.chdir(bin)
    os.mkdir(riderdir)
    subprocess.check_call(['tar', 'xvzf', downloads+'/'+riderzip, '-C', riderdir, '--strip-component=1'])

    os.chdir(path)
    output('- Rider installed ......: <green>Done<nc>')

def install_pycharm(targetsys, options, downloads, bin):
    output('- install PyCharm.......: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.pycharm, options.nopycharm):
        output('<yellow>pass<nc>')
        return

    charmdir = bin + '/Jetbrains.PyCharm'
    if os.path.isdir(charmdir):
        output('<yellow>already installed<nc>')
        return
    path = os.getcwd()
    os.chdir(downloads)
    charmzip = 'pycharm-community-2020.3.2.tar.gz'
    if not os.path.isfile(charmzip):
        subprocess.check_call(['wget', 'https://download.jetbrains.com/python/'+charmzip])
    os.chdir(bin)
    os.mkdir(charmdir)
    subprocess.check_call(['tar', 'xvzf', downloads+'/'+charmzip, '-C', charmdir, '--strip-component=1'])
    #subprocess.check_call(['mv', 'pycharm-community*', charmdir])

    os.chdir(path)
    output('- PyCharm installed.....: <green>Done<nc>')

def install_clion(targetsys, options, downloads, bin):
    output('- install CLion.........: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.clion, options.noclion):
        output('<yellow>pass<nc>')
        return

    cliondir = bin + '/Jetbrains.CLion'
    if os.path.isdir(cliondir):
        output('<yellow>already installed<nc>')
        return
    path = os.getcwd()
    os.chdir(downloads)
    clionzip = 'CLion-2020.3.1.tar.gz'
    if not os.path.isfile(clionzip):
        subprocess.check_call(['wget', 'https://download.jetbrains.com/cpp/'+clionzip])
    os.chdir(bin)
    os.mkdir(cliondir)
    subprocess.check_call(['tar', 'xvzf', downloads+'/'+clionzip, '-C', cliondir, '--strip-component=1'])

    os.chdir(path)
    output('- CLion installed.......: <green>Done<nc>')

def install_webstorm(targetsys, options, downloads, bin):
    output('- install WebStorm......: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.storm, options.nostorm):
        output('<yellow>pass<nc>')
        return

    stormdir = bin + '/Jetbrains.WebStorm'
    if os.path.isdir(stormdir):
        output('<yellow>Already installed<nc>')
        return
    path = os.getcwd()
    os.chdir(downloads)
    stormzip = 'WebStorm-2020.3.1.tar.gz'
    if not os.path.isfile(stormzip):
        subprocess.check_call(['wget', 'https://download.jetbrains.com/webstorm/'+stormzip])
    os.chdir(bin)
    os.mkdir(stormdir)
    subprocess.check_call(['tar', 'xvzf', downloads+'/'+stormzip, '-C', stormdir, '--strip-component=1'])

    os.chdir(path)
    output('- WebStorm installed....: <green>Done<nc>')

def install_code(targetsys, options, downloads, bin):
    output('- install VS Code ......: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.code, options.nocode):
        output('<yellow>pass<nc>')
        return

    code = os.popen('which code').read()[:-1]
    if "/code" in code:
        output('<yellow>Already installed<nc>')
        return

    if targetsys == Systems.SuSE or targetsys == targetsys == Systems.Fedora:
        subprocess.check_call(['sudo', 'rpm', '--import', 'https://packages.microsoft.com/keys/microsoft.asc'])
        subprocess.check_call(['sudo', 'sh', '-c', 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'])
        subprocess.check_call(['sudo', 'dnf', 'check-update'])
        subprocess.check_call(['sudo', 'dnf', 'install', 'code'])
    elif targetsys == Systems.Ubuntu or targetsys == Systems.Zorin:
        path = os.getcwd()
        os.chdir(downloads)
        subprocess.check_call(['wget', '-q0-', 'https://packages.microsoft.com/keys/microsoft.asc', '|', 'gpg', '--dearmor', '>', 'packages.microsoft.gpg'])
        subprocess.check_call(['sudo', 'install', '-o', 'root', '-g', 'root', '-m', '644', 'packages.microsoft.gpg', '/etc/apt/trusted.gpg.d/'])
        subprocess.check_call(['sudo', 'sh', '-c', 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'])
        subprocess.check_call(['sudo', 'apt', 'install', 'apt-transport-https'])
        subprocess.check_call(['sudo', 'apt', 'update'])
        subprocess.check_call(['sudo', 'apt', 'install', 'code'])
        os.chdir(path)
    else:
      output('<red>unsupported<nc>')
      return

    output('- VS Code installed .....: <green>Done<nc>')

def install_keybase(targetsys, downloads):
    output('- Installing keybase ...: ', False)

    flow = os.popen('which keybase').read()[:-1]
    if "/keybase" in flow:
        output('<yellow>Already installed<nc>')
        return

    path = os.getcwd()
    os.chdir(downloads)

    if targetsys == Systems.SuSE or targetsys == Systems.Fedora:
        subprocess.check_call(['sudo', 'dnf', 'install', 'y', 'https://prerelease.keybase.io/keybase_amd64.rpm'])
    elif targetsys == Systems.Ubuntu or targetsys == Systems.Zorin:
        subprocess.check_call(['curl', '-remote-name', 'https://prerelease.keybase.io/keybase_amd64.de'])
        subprocess.check_call(['sudo', 'apt', 'install', './keybase_amd64.deb'])
    else:
        os.chdir(path)
        output('<red>unsupported<nc>')
        return

    subprocess.check_call(['run_keybase'])

    os.chdir(path)
    output('<green>Done<nc>')


def install_externals(targetsys, subsys, options):
    # [0.3] cygwin                  [0.B] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.5] Ubuntu
    # [ ] Fedora                    [0.7] Zorin
    output('Install externals.......: ', False)
    #if not options.externals or (options.full and options.noexternals):
    if subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.externals, options.noexternals):
        output('<yellow>pass<nc>')
        return
    output('')
    downloads = get_downloads()
    work = str(Path.home()) + '/work'
    bin = str(Path.home()) + '/bin'

    install_keybase(targetsys, downloads)
    install_qt(targetsys, options, downloads, work)
    install_rider(targetsys, options, downloads, bin)
    install_pycharm(targetsys, options, downloads, bin)
    install_clion(targetsys, options, downloads, bin)
    install_webstorm(targetsys, options, downloads, bin)
    install_code(targetsys, options, downloads, bin)

    output('Externals installed.....: <green>Done<nc>')

#endregion

def install_all(targetsys, subsys, installprog, options):
    # [0.3] cygwin                  [0.B] Fedora
    # [ ] macos                     [ ] SuSE
    # [ ] FreeBSD                   [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.5] Ubuntu
    # [ ] Fedora                    [0.7] Zorin
    install_core(installprog, targetsys, subsys, options)
    install_dotfiles(options)
    install_zsh(targetsys, options)
    install_prezto(targetsys, options)
    install_login(targetsys, subsys, options)
    install_links(targetsys, subsys, options)
    install_fonts(targetsys, subsys, options)

    # create_ssh_key
    packages = install_basics(targetsys, subsys, options)
    packages += install_nextcloud(targetsys, subsys, options)
    packages += install_programs(targetsys, subsys, options)
    packages += install_xprograms(targetsys, subsys, options)
    packages += install_compiler(targetsys, subsys, options)
    packages += install_xfce_programs(targetsys, subsys, options)
    packages += install_tex(targetsys, subsys, options)
    packages += install_games(targetsys, subsys, options)
    if packages:
      output('Installing programs ....: ', False)
      install(installprog, packages)
      output('<green>Done<nc>')
    install_dotnet(installprog, targetsys, options)

    install_externals(targetsys, subsys, options)
    install_gitflow()
    clone_all(options)

output("<head>=====[ Configuring system ]====<nc>")
(system,subsys) = determine_os()
if system is None:
    quit()
installer = determine_installer(system)
args = create_parser()

#output(f'Systems is <green>{system}<nc> with installer <tc>{installer}<nc>')
#copy_text_to_clipboard(system, 'This is a test clip')
#ensure_root(system)
install_all(system, subsys, installer, args)
