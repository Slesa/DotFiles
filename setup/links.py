# [11] Fedora             [12] FreeBSD        [13] NetBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin                  
# [  ] SuSE               [  ] Arch / Manjaro
import os
from pathlib import Path
from setup.osplatform import Systems, Subsys
from setup.console import output
from setup.helpers import flag_is_set


def link_file(source, target):
    if not os.path.islink(target):
        os.symlink(source, target)

def link_unix_target(source, target, filename):
    targetdir = os.path.dirname(target)
    if not os.path.isdir(targetdir):
        os.mkdir(targetdir)

    link_file(source + filename, target)


def link_unix_config(root, filename, folder=''):
    source = root + '/etc/unix/'
    if folder:
        source = source + folder + '/'
    target = '/.config/' + filename
    target = str(Path.home()) + target
    link_unix_target(source, target, filename)


def link_unix_file(root, filename, folder=''):
    source = root + '/etc/unix/'
    if folder:
        source = source + folder + '/'
    target = '/.' + filename
    target = str(Path.home()) + target
    link_unix_target(source, target, filename)



def link_autostart(root, filename):
    target = str(Path.home()) + '/.config/autostart/' + filename
    if not os.path.islink(target):
        source = root + '/etc/unix/autostart/' + filename
        os.symlink(source, target)


def link_unix_files(root):
    link_unix_file(root, 'zsh')
    link_unix_config(root, 'nvim')
    link_unix_config(root, 'i3')
    link_unix_file(root, 'tmux.conf')
    link_unix_file(root, 'gitconfig')
    link_unix_file(root, 'vimrc')
    link_unix_file(root, 'taskrc')
    link_unix_file(root, 'zprofile', 'zprezto')
    link_unix_file(root, 'zlogin', 'zprezto')
    link_unix_file(root, 'zlogout', 'zprezto')
    link_unix_file(root, 'zpreztorc', 'zprezto')
    link_unix_file(root, 'zshenv', 'zprezto')
    link_unix_file(root, 'p10k.zsh', 'zprezto')


# [11] Fedora             [12] FreeBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin
# [  ] SuSE               [  ] Arch / Manjaro
def install_links(root, targetsys, subsys, options):
    output('Install Links...........: ', False)
    if not flag_is_set(options, options.links, options.nolinks):
        output('<yellow>pass<nc>')
        return
    bindir = str(Path.home()) + '/bin'
    if not os.path.isdir(bindir):
        os.mkdir(bindir)
    if not os.path.islink(bindir + '/tools'):
        os.symlink(root + '/bin/tools', bindir + '/tools')

    link_unix_files(root)

    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<green>Ok<nc>')
        return

    link_file('data/img/avatar.png', str(Path.home()) + '/.face')
    # Autostart
    autosource = root + '/etc/unix/autostart/'
    autostart = str(Path.home()) + '/.config/autostart/'
    if not os.path.isdir(autostart):
        os.mkdir(autostart)
    link_autostart(root, 'nextCloud.desktop')
    link_autostart(root, 'Thunderbird.desktop')
    link_autostart(root, 'Hexchat.desktop')

    output('<green>Ok<nc>')
