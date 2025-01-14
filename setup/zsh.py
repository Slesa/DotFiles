# [11] Fedora             [12] FreeBSD        [13] NetBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin                  
# [  ] SuSE               [  ] Arch / Manjaro
import os
import subprocess
from pathlib import Path
from setup.osplatform import Systems
from setup.console import output
from setup.helpers import flag_is_set


def install_zsh(root, targetsys, options):
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
        elif targetsys == Systems.NetBSD:
            srcfile = 'zshrc.freebsd'
        elif targetsys == Systems.OpenBSD:
            srcfile = 'zshrc.freebsd'
        elif targetsys == Systems.FreeBSD:
            srcfile = 'zshrc.freebsd'
        elif targetsys == Systems.Arch:
            srcfile = 'zshrc.manjaro'
        elif targetsys == Systems.Raspbian:
            srcfile = 'zshrc.raspbian'
#        elif targetsys == Systems.SunOS:
#            srcfile = 'zshrc.sunos'
        elif targetsys == Systems.Fedora or targetsys == Systems.Mageia:
            srcfile = 'zshrc.fedora'
        elif targetsys == Systems.Ubuntu or targetsys == Systems.Zorin:
            srcfile = 'zshrc.ubuntu'
        else:
            srcfile = 'zshrc.ubuntu'
        subprocess.check_call(['cp', root + '/data/templ/' + srcfile, targetfile])
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
