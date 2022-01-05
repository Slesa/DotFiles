# [11] Fedora             [12] FreeBSD        [13] NetBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin                  
# [  ] SuSE               [  ] Arch / Manjaro
import os
import subprocess
from pathlib import Path
from setup.console import output
from setup.helpers import flag_is_set


def install_prezto(_, options):
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
