# [11] Fedora             [15] RHEL/Alma       [14] SuSE
# [12] FreeBSD            [13] NetBSD
# [05] Xubuntu            [  ] MX              [16] Mageia
# [02] Ubuntu on Windows  [03] Cygwin          [  ] Arch / Manjaro
import os
import subprocess
from pathlib import Path
from setup.osplatform import Systems, Subsys
from setup.console import output
from setup.helpers import flag_is_set, flag_is_set_explicit

#region Bitbucket

def clone_from_bitbucket(src, project, flow, base=''):
    if os.path.isdir(src + project):
        return
    header = 'git@' if '/' not in project else 'https://'
    target = ':slesa1/'+project if '/' not in project else '/'+project+'.git'
    subprocess.check_call(['git', 'clone', header + 'bitbucket.org' + target])
    if base:
        os.system('cd '+project+f" && git remote add upstream {base} && cd ..")
    if flow:
        os.system('cd '+project+" && git flow init -d && git checkout develop && cd ..")


def clone_apostel_from_bitbucket(root):
    src = root + "/bitbucket/apostel/"
    if not os.path.isdir(src):
        os.mkdir(src)

    os.chdir(src)
    clone_from_bitbucket(src, 'Apostel-net', False)
    clone_from_bitbucket(src, 'Apostel-rust', False)
    clone_from_bitbucket(src, 'Apostel-qt', False)
    #clone_recursive_github(src, 'Apostel', False)
    os.chdir('..')
    os.chdir('..')


def clone_bitbucket(root, targetsys, options):
    output('Clone bitbucket ........: ', False)
    if not flag_is_set_explicit(options.bitbucket, options.nobitbucket, True):
        output('<yellow>pass<nc>')
        return
    src = root + "/bitbucket/"
    if not os.path.isdir(src):
        os.mkdir(src)

    os.chdir(src)
    clone_from_bitbucket(src, 'poseidon', True)
    clone_from_bitbucket(src, 'apostel', True)
    os.chdir('..')
    clone_apostel_from_bitbucket(root)

    output('<green>Done<nc>')

#endregion Bitbucket


#region Github

def clone_it_from_github(src, project, flow, recursive, base=''):
    if os.path.isdir(src + project):
        return
    header = 'git@' if '/' not in project else 'https://'
    target = ':slesa/'+project if '/' not in project else '/'+project
    if recursive:
        subprocess.check_call(['git', 'clone', '--recurse-modules', header + 'github.com' + target])
    else:    
        subprocess.check_call(['git', 'clone', header + 'github.com' + target])
    if base:
        os.system('cd '+project+f" && git remote add upstream {base} && cd ..")
    if flow:
        os.system('cd '+project+" && git flow init -d && git checkout develop && cd ..")


def clone_recursive_github(src, project, flow, base=''):
    clone_it_from_github(src, project, flow, True, base)

def clone_from_github(src, project, flow, base=''):
    clone_it_from_github(src, project, flow, False, base)


def clone_apostel_from_github(root):
    src = root + "/github/apostel/"
    if not os.path.isdir(src):
        os.mkdir(src)

    os.chdir(src)
    clone_from_github(src, 'Apostel-net', False)
    clone_from_github(src, 'Apostel-rust', False)
    clone_from_github(src, 'Apostel-qt', False)
    clone_recursive_github(src, 'Apostel', False)
    os.chdir('..')
    os.chdir('..')


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
    src = root + "/os/"
    if not os.path.isdir(src):
        os.mkdir(src)

    os.chdir(src)
    clone_from_github(src, 'freebsd-ports', True)
    clone_from_github(src, 'freebsd-ports-dosbox-x', True)
    clone_from_github(src, 'dosbox-x', True)
    os.chdir('..')
    os.chdir('..')


def clone_oi_from_github(root):
    src = root + "/os/"
    if not os.path.isdir(src):
        os.mkdir(src)

    os.chdir(src)
    clone_from_github(src, 'oi-userland', True)
    os.chdir('..')
    os.chdir('..')

def clone_github(root, targetsys, options):
    output('Clone github ...........: ', False)
    if not flag_is_set_explicit(options.github, options.nogithub, True):
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
    clone_apostel_from_github(root)
    clone_safe_from_github(root)
    if targetsys == Systems.BSD or targetsys == Systems.SunOS:
        clone_bsd_from_github(root)
    if targetsys == Systems.SunOS:
        clone_oi_from_github(root)

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
    if not flag_is_set_explicit(options.gitlab, options.nogitlab, True):
        output('<yellow>pass<nc>')
        return
    src = root + "/gitlab/"
    if not os.path.isdir(src):
        os.mkdir(src)

    os.chdir(src)
    #clone_from_gitlab(src, 'waiterwatch', True)
    #clone_from_gitlab(src, 'aikidoka', True)
    #clone_from_gitlab(src, 'monty', False)
    #clone_from_gitlab(src, 'ravebase', False)
    clone_from_gitlab(src, 'Sketches', False)
    clone_from_gitlab(src, 'Poseidon', False)
    clone_from_gitlab(src, 'japanisch', False)
    os.chdir('..')
    # clone_xfce_from_gitlab(root)

    output('<green>Done<nc>')

#endregion


def clone_all(targetsys, options):
    output('Cloning sources.........: ', False)
    if not flag_is_set(options, options.clone, options.noclone):
        output('<yellow>pass<nc>')
        return
    output('')
    src = str(Path.home()) + '/work'
    if not os.path.isdir(src):
        os.mkdir(src)
    clone_bitbucket(src, targetsys, options)
    clone_github(src, targetsys, options)
    clone_gitlab(src, options)

    output('<green>Done<nc>')
