import os
import subprocess
from pathlib import Path
from setup.osplatform import Systems, Subsys
from setup.console import output
from setup.helpers import flag_is_set


# region Github

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


def clone_bsd_from_github(root):
    src = root + "/bsd/"
    if not os.path.isdir(src):
        os.mkdir(src)

    os.chdir(src)
    clone_from_github(src, 'freebsd-ports-dosbox-x', True)
    clone_from_github(src, 'dosbox-x', True)
    os.chdir('..')
    os.chdir('..')


def clone_github(root, targetsys, options):
    output('Clone github ...........: ', False)
    if not flag_is_set(options, options.github, options.nogithub):
        output('<yellow>pass<nc>')
        return
    src = root + "/github/"
    if not os.path.isdir(src):
        os.mkdir(src)

    os.chdir(src)
    clone_from_github(src, 'Poseidon', True)
    clone_from_github(src, 'sqlitestudio', True)
    clone_from_github(src, 'Trinity', True)
    clone_from_github(src, 'Godot', False)
    clone_from_github(src, 'FsReveal', False)

    clone_from_github(src, 'FAKE', True, 'https://github.com/fsharp/FAKE.git')
    clone_from_github(src, 'machine.specifications', True, 'https://github.com/machine/machine.specifications.git')
    clone_from_github(src, 'EventStore', True, 'https://github.com/EventStore/EventStore.git')

    os.chdir('..')
    clone_safe_from_github(root)
    if targetsys == Systems.BSD:
        clone_bsd_from_github(root)

    output('<green>Done<nc>')

# endregion

# region Gitlab


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
    clone_from_gitlab(src, 'Poseidon', False)
    os.chdir('..')
    # clone_xfce_from_gitlab(root)

    output('<green>Done<nc>')

# endregion

# region 42 repos


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
    clone_from_gf(src, 'mke', 'mke-fo', True)
    # clone_from_gf(src, 'mat', 'matrixodooaddons', False)
    # clone_from_gf(src, 'mat', 'matrixbackoffice', False)
    # clone_from_gf(src, 'mat', 'tseconnector', False)
    clone_from_gf(src, 'bv', 'playground', False)
    os.chdir('..')

    output('<green>Done<nc>')

# endregion


# [11] Fedora             [12] FreeBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin
# [  ] SuSE               [  ] Arch / Manjaro
def clone_all(targetsys, options):
    output('Cloning sources.........: ', False)
    if not flag_is_set(options, options.clone, options.noclone):
        output('<yellow>pass<nc>')
        return
    output('')
    src = str(Path.home()) + '/work'
    if not os.path.isdir(src):
        os.mkdir(src)
    clone_github(src, targetsys, options)
    clone_gitlab(src, options)
    clone_gf(src, options)

    output('<green>Done<nc>')