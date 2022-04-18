import os
import subprocess
from pathlib import Path
from setup.osplatform import Systems, Subsys
from setup.console import output
from setup.helpers import flag_is_set, get_downloads, install


def install_keybase(targetsys, downloads):
    output('- Installing keybase ...: ', False)

    flow = os.popen('which keybase').read()[:-1]
    if "/keybase" in flow:
        output('<yellow>Already installed<nc>')
        return

    path = os.getcwd()
    os.chdir(downloads)

    if targetsys == Systems.SuSE or targetsys == Systems.Fedora:
        subprocess.check_call(['sudo', 'dnf', 'install', '-y', 'https://prerelease.keybase.io/keybase_amd64.rpm'])
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


def install_brave(installprog, targetsys, options):
    output('- install Brave Browser : ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.brave, options.nobrave):
         output('<yellow>pass<nc>')
         return

    code = os.popen('which brave-browser').read()[:-1]
    if "/brave" in code:
        output('<yellow>Already installed<nc>')
        return
    if targetsys == Systems.SuSE: 
        subprocess.check_call(['sudo', 'zypper', 'addrepo', 'https://brave-browser-rpm-release.s3.brave.com/x86_64/', 'brave-browser'])
        subprocess.check_call(['sudo', 'rpm', '--import', 'https://brave-browser-rpm-release.s3.brave.com/brave-core.asc'])
        install(installprog, ['brave-browser'])
    elif targetsys == targetsys == Systems.Fedora:
        subprocess.check_call(['sudo', 'dnf', 'config-manager', '--add-repo', 'https://brave-browser-rpm-release.s3.brave.com/x86_64/'])
        subprocess.check_call(['sudo', 'rpm', '--import', 'https://brave-browser-rpm-release.s3.brave.com/brave-core.asc'])
        install(installprog, ['brave-browser'])
        #subprocess.check_call(['sudo', 'dnf', 'install', '-y', 'brave-browser'])
    # elif targetsys == Systems.Ubuntu or targetsys == Systems.Zorin:
    else:
        output('<red>unsupported<nc>')
        return

    output('- Brave Browser ........: <green>Done<nc>')


def install_qt(targetsys, options, downloads, work):
    output('- install Qt ...........: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if targetsys == Systems.BSD:
        output('<tc>not supported<nc>')
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
    # copy_text_to_clipboard(targetsys, work+'/qt')
    subprocess.Popen(['./'+qtinstaller])

    os.chdir(path)
    output('- Qt installed .........: <green>Done<nc>')


# region JetBrains

def install_jetbrain(tool, zipfile, target, downloads, bindir):
    tooldir = bindir + '/Jetbrains.'+tool
    if os.path.isdir(tooldir):
        output('<yellow>already installed<nc>')
        return False
    path = os.getcwd()
    os.chdir(downloads)
    if not os.path.isfile(zipfile):
        subprocess.check_call(['wget', 'https://download.jetbrains.com/'+target+'/'+zipfile])
    os.chdir(bindir)
    os.mkdir(tooldir)
    subprocess.check_call(['tar', 'xvzf', downloads+'/'+zipfile, '-C', tooldir, '--strip-component=1'])
    os.chdir(path)
    return True


def install_rider(targetsys, options, downloads, bindir):
    output('- install Rider.........: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.rider, options.norider):
        output('<yellow>pass<nc>')
        return
    riderzip = 'JetBrains.Rider-2021.3.4.tar.gz'
    if install_jetbrain('Rider', riderzip, 'rider', downloads, bindir):
        return
    output('- Rider installed ......: <green>Done<nc>')


def install_pycharm(targetsys, options, downloads, bindir):
    output('- install PyCharm.......: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.pycharm, options.nopycharm):
        output('<yellow>pass<nc>')
        return
    charmzip = 'pycharm-professional-2022.1.tar.gz'
    if install_jetbrain('PyCharm', charmzip, 'python', downloads, bindir):
        return
    output('- PyCharm installed.....: <green>Done<nc>')


def install_clion(targetsys, options, downloads, bindir):
    output('- install CLion.........: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.clion, options.noclion):
        output('<yellow>pass<nc>')
        return
    clionzip = 'CLion-2022.1.tar.gz'
    if install_jetbrain('CLion', clionzip, 'cpp', downloads, bindir):
        return
    output('- CLion installed.......: <green>Done<nc>')


def install_webstorm(targetsys, options, downloads, bindir):
    output('- install WebStorm......: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.storm, options.nostorm):
        output('<yellow>pass<nc>')
        return
    stormzip = 'WebStorm-2022.1.tar.gz'
    if install_jetbrain('WebStorm', stormzip, 'webstorm', downloads, bindir):
        return
    output('- WebStorm installed....: <green>Done<nc>')

# endregion JetBrains


def install_code(installprog, targetsys, options, downloads, bindir):
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

    if targetsys == Systems.SuSE:
        subprocess.check_call(['sudo', 'rpm', '--import', 'https://packages.microsoft.com/keys/microsoft.asc'])
        subprocess.check_call(['sudo', 'zypper', 'addrepo', 'https://packages.microsoft.com/yumrepos/vscode', 'vscode'])
        subprocess.check_call(['sudo', 'zypper', 'refresh'])
        install(installprog, ['code'])
    elif targetsys == Systems.Fedora:
        subprocess.check_call(['sudo', 'rpm', '--import', 'https://packages.microsoft.com/keys/microsoft.asc'])
        subprocess.check_call(['sudo', 'sh', '-c', 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'])
        subprocess.check_call(['sudo', 'dnf', 'check-update'])
        install(installprog, ['code'])
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


def install_gitflow(targetsys):
    if targetsys == Systems.BSD:
        return
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


# [13] Fedora             [12] FreeBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin
# [14] SuSE               [  ] Arch / Manjaro
def install_externals(installprog, targetsys, subsys, options):
    output('Install externals.......: ', False)
    if subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.externals, options.noexternals):
        output('<yellow>pass<nc>')
        return
    output('')
    downloads = get_downloads()
    work = str(Path.home()) + '/work'
    bindir = str(Path.home()) + '/bin'

    #install_keybase(targetsys, downloads)
    install_brave(installprog, targetsys, options)
    install_qt(targetsys, options, downloads, work)
    install_rider(targetsys, options, downloads, bindir)
    install_pycharm(targetsys, options, downloads, bindir)
    install_clion(targetsys, options, downloads, bindir)
    install_webstorm(targetsys, options, downloads, bindir)
    install_code(installprog, targetsys, options, downloads, bindir)
    install_gitflow(targetsys)

    output('Externals installed.....: <green>Done<nc>')
