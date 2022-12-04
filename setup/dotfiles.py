import os
import subprocess
from setup.console import output
from setup.helpers import flag_is_set


# [11] Fedora             [12] FreeBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin
# [  ] SuSE               [  ] Arch / Manjaro
def install_dotfiles(rootpath, options):
    output('Install dotfiles........: ', False)
    if not flag_is_set(options, options.dotfiles, options.nodotfiles):
        output('<yellow>pass<nc>')
        return
    if os.path.isdir(rootpath):
        output('<green>already installed, updating...')
        subprocess.check_call(['git', 'pull', 'origin', 'main'])
        output('done<nc>')
        return
    output('<tc>cloning<nc>')
    subprocess.check_call(['git', 'clone', 'git@github.com:slesa/DotFiles', Basepath])
    output('Dotfiles installed......: <green>Done<nc>')
