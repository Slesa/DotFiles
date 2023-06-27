import os
import subprocess
from pathlib import Path
from setup.osplatform import Systems
from setup.console import output


def get_pid(name):
    try:
        return subprocess.check_output(["pidof", "-s", name])
    except subprocess.CalledProcessError:
        return 0


def copy_text_to_clipboard(os, text):
    if os == Systems.MacOS:
        subprocess.Popen(('pbcopy', text))
    elif os == Systems.Cygwin:
        subprocess.run(f'echo {text} > /dev/clipboard')
    else:
        subprocess.Popen(('xsel', '--clipboard', text))
        # cat = subprocess.Popen(('echo', f'"{text}"'), stdout=subprocess.PIPE)
        # output = subprocess.check_output(('xsel', '--clipboard'), stdin=cat.stdout)
        # cat.wait()
        # subprocess.run(['cat', '"{text}"', '\|', 'xsel', '--clipboard'])


def ensure_root(osys):
    import getpass
    output('Checking root access....: ', False)
    if osys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return

    if not os.geteuid()==0:
        # output('<yellow>have to ask<nc>')
        # sudopw = getpass.getpass('Enter sudo password.....: ')
        sudopw = getpass.getpass()
        command = 'ls > /dev/null'
        os.system('echo %s|sudo -S %s' % (sudopw, command))
    # subprocess.Popen('sudo', shell=True)
    output('<green>Ok<nc>')


def install(installprog, packages):
    print(installprog)
    print(packages)
    subprocess.check_call(installprog + packages)


def flag_is_set_def_false(options, on_flag, off_flag):
    if off_flag:
        return False
    if options.full and not on_flag:
        return False
    return True


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
