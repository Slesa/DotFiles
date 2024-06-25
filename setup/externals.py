# [11] Fedora             [15] RHEL/Alma       [14] SuSE
# [12] FreeBSD            [13] NetBSD
# [05] Xubuntu            [  ] MX              [16] Mageia
# [02] Ubuntu on Windows  [03] Cygwin          [  ] Arch / Manjaro
import os
import subprocess
from pathlib import Path
from setup.osplatform import Systems, Subsys
from setup.console import output
from setup.helpers import flag_is_set, flag_is_set_explicit, get_downloads, install


class Externals:
    def __init__(self, installprog, targetsys, subsys, options):
        self.installprog = installprog
        self.targetsys = targetsys
        self.subsys = subsys
        self.options =  options
        self.downloads = get_downloads()
        self.work = str(Path.home()) + '/work'
        self.bindir = str(Path.home()) + '/bin'

    def install_keybase(self):
        if not flag_is_set_explicit(self.options.keybase, self.options.nokeybase, True):
            output('<yellow>pass<nc>')
            return []
        output('- Installing keybase ...: ', False)

        flow = os.popen('which keybase').read()[:-1]
        if "/keybase" in flow:
            output('<yellow>Already installed<nc>')
            return

        path = os.getcwd()
        os.chdir(self.downloads)

        if self.targetsys == Systems.SuSE:
            install(self.installprog, ['keybase-client'])
        else:
            if self.targetsys == Systems.Fedora or self.targetsys == Systems.Redhat or self.targetsys == Systems.Mageia:
                subprocess.check_call(['sudo', 'dnf', 'install', '-y', 'https://prerelease.keybase.io/keybase_amd64.rpm'])
            elif self.targetsys == Systems.Ubuntu:
                subprocess.check_call(['curl', '-remote-name', 'https://prerelease.keybase.io/keybase_amd64.de'])
                subprocess.check_call(['sudo', 'apt', 'install', './keybase_amd64.deb'])
            else:
                os.chdir(path)
                output('<red>unsupported<nc>')
                return
            subprocess.check_call(['run_keybase'])

        os.chdir(path)
        output('<green>Done<nc>')


    def install_brave(self):
        output('- install Brave Browser : ', False)
        if self.targetsys == Systems.Cygwin or self.targetsys == Systems.Arch:
            output('<tc>not necessary<nc>')
            return
        if not flag_is_set_explicit(self.options.brave, self.options.nobrave, True):
            output('<yellow>pass<nc>')
            return

        code = os.popen('which brave-browser').read()[:-1]
        if "/brave" in code:
            output('<yellow>Already installed<nc>')
            return
        if self.targetsys == Systems.SuSE: 
            subprocess.check_call(['sudo', 'zypper', 'addrepo', 'https://brave-browser-rpm-release.s3.brave.com/x86_64/', 'brave-browser'])
            subprocess.check_call(['sudo', 'rpm', '--import', 'https://brave-browser-rpm-release.s3.brave.com/brave-core.asc'])
            subprocess.check_call(['sudo', 'zypper', 'refresh'])
            install(self.installprog, ['brave-browser'])
        elif self.targetsys == Systems.Mageia or self.targetsys == Systems.Fedora or self.targetsys == Systems.Redhat:
            subprocess.check_call(['sudo', 'dnf', 'config-manager', '--add-repo', 'https://brave-browser-rpm-release.s3.brave.com/x86_64/'])
            subprocess.check_call(['sudo', 'rpm', '--import', 'https://brave-browser-rpm-release.s3.brave.com/brave-core.asc'])
            install(self.installprog, ['brave-browser'])
            #subprocess.check_call(['sudo', 'dnf', 'install', '-y', 'brave-browser'])
        # elif targetsys == Systems.Ubuntu or targetsys == Systems.Zorin:
        else:
            output('<red>unsupported<nc>')
            return

        output('- Brave Browser ........: <green>Done<nc>')


    def install_iridium(self):
        output('- install Iridium.......: ', False)
        if self.targetsys == Systems.Cygwin or self.targetsys == Systems.Arch:
            output('<tc>not necessary<nc>')
            return
        if not flag_is_set_explicit(self.options.iridium, self.options.noiridium, True):
            output('<yellow>pass<nc>')
            return

        code = os.popen('which iridium-browser').read()[:-1]
        if "/iridium" in code:
            output('<yellow>Already installed<nc>')
            return
        if self.targetsys == Systems.SuSE: 
            subprocess.check_call(['sudo', 'zypper', 'addrepo', 'https://downloads.iridiumbrowser.de/openSUSE_Leap_15.5/', 'iridium'])
            subprocess.check_call(['sudo', 'zypper', 'refresh'])
            install(self.installprog, ['iridium-browser'])
        elif self.targetsys == Systems.Mageia or self.targetsys == Systems.Fedora or self.targetsys == Systems.Redhat:
            subprocess.check_call(['sudo', 'dnf', 'config-manager', '--add-repo', 'https://dl.iridiumbrowser.de/fedora_39/iridium-browser.repo'])
            install(self.installprog, ['iridium-browser'])
        else:
            output('<red>unsupported<nc>')
            return

        output('- Iridium Browser ......: <green>Done<nc>')


    def install_qt(self):
        output('- install Qt ...........: ', False)
        if self.targetsys == Systems.Cygwin:
            output('<tc>not necessary<nc>')
            return
        if self.targetsys == Systems.BSD:
            output('<tc>not supported<nc>')
            return
        if not flag_is_set_explicit(self.options.qt, self.options.noqt, True):
            output('<yellow>pass<nc>')
            return

        if os.path.isdir(self.work+'/Qt') or os.path.isdir(self.work+'/qt'):
            output('<yellow>already installed<nc>')
            return
        path = os.getcwd()
        os.chdir(self.downloads)

        qtinstaller = 'qt-unified-linux-x64-online.run'
        if self.targetsys==Systems.Cygwin:
            qtinstaller = 'qt-unified-windows-x86-online.exe'
        elif self.targetsys==Systems.MacOS:
            qtinstaller = 'qt-unified-mac-x64-online.dmg'
        if not os.path.isfile(qtinstaller):
            subprocess.check_call(['wget', 'https://download.qt.io/official_releases/online_installers/'+qtinstaller])
            subprocess.check_call(['chmod', '+x', qtinstaller])
        # copy_text_to_clipboard(targetsys, work+'/qt')
        subprocess.Popen(['./'+qtinstaller])

        os.chdir(path)
        output('- Qt installed .........: <green>Done<nc>')


# region JetBrains

    def install_jetbrain(self, tool, zipfile, target, cdn=False):
        tooldir = self.bindir + '/Jetbrains.'+tool
        if os.path.isdir(tooldir):
            output('<yellow>already installed<nc>')
            return False
        path = os.getcwd()
        os.chdir(self.downloads)
        if not os.path.isfile(zipfile):
            url = 'https://download.jetbrains.com/' if cdn else 'https://download-cdn.jetbrains.com/'
            subprocess.check_call(['wget', 'https://download.jetbrains.com/'+target+'/'+zipfile])
        os.chdir(self.bindir)
        os.mkdir(tooldir)
        subprocess.check_call(['tar', 'xvzf', self.downloads+'/'+zipfile, '-C', tooldir, '--strip-component=1'])
        os.chdir(path)
        return True


    def link_jetbrain(self, tool, sh):
        linksh = '/usr/local/bin/'+sh
        if not os.path.exists(linksh):
            toolsh = self.bindir + '/Jetbrains.'+tool+'/bin/'+sh+'.sh'
            subprocess.check_call(['sudo', 'ln', '-s', toolsh, linksh])
        else:
            output('<yellow>symlink '+tool+' already exists<nc>')



    def install_toolbox(self):
        output('- install Toolbox.......: ', False)
        if self.targetsys == Systems.BSD:
            output('<tc>not supported<nc>')
            return
        if self.targetsys == Systems.Cygwin:
            output('<tc>not necessary<nc>')
            return
        if not flag_is_set_explicit(self.options.toolbox, self.options.notoolbox, True):
            output('<yellow>pass<nc>')
            return
        toolboxzip = 'jetbrains-toolbox-2.3.2.31487.tar.gz'
        if self.install_jetbrain('Toolbox', toolboxzip, 'toolbox', True):
            return
        output('- Toolbox installed ....: <green>Done<nc>')


    def install_rider(self):
        output('- install Rider.........: ', False)
        if self.targetsys == Systems.Cygwin:
            output('<tc>not necessary<nc>')
            return
        if not flag_is_set_explicit(self.options.rider, self.options.norider, self.targetsys==Systems.BSD):
            output('<yellow>pass<nc>')
            return
        riderzip = 'JetBrains.Rider-2024.1.4.tar.gz'
        if self.install_jetbrain('Rider', riderzip, 'rider'):
            return
        self.link_jetbrain('Rider', 'rider')
        output('- Rider installed ......: <green>Done<nc>')

    def install_rover(self):
        output('- install Rust Rover....: ', False)
        #https://download.jetbrains.com/rustrover/RustRover-233.10527.39-aarch64.tar.gz
        if self.targetsys == Systems.Cygwin:
            output('<tc>not necessary<nc>')
            return
        if not flag_is_set_explicit(self.options.rover, self.options.norover, self.targetsys == Systems.BSD):
            output('<yellow>pass<nc>')
            return
        roverzip = 'RustRover-2024.1.3.tar.gz'
        if self.install_jetbrain('Rover', roverzip, 'rustrover'):
            return
        self.link_jetbrain('Rover', 'rustrover')
        output('- Rust Rover installed .: <green>Done<nc>')

    def install_pycharm(self):
        output('- install PyCharm.......: ', False)
        if self.targetsys == Systems.Cygwin:
            output('<tc>not necessary<nc>')
            return
        if not flag_is_set_explicit(self.options.pycharm, self.options.nopycharm, self.targetsys == Systems.BSD):
            output('<yellow>pass<nc>')
            return
        charmzip = 'pycharm-professional-2024.1.4.tar.gz'
        if self.install_jetbrain('PyCharm', charmzip, 'python'):
            return
        self.link_jetbrain('PyCharm', 'pycharm')
        output('- PyCharm installed.....: <green>Done<nc>')


    def install_clion(self):
        output('- install CLion.........: ', False)
        if self.targetsys == Systems.Cygwin:
            output('<tc>not necessary<nc>')
            return
        if not flag_is_set_explicit(self.options.clion, self.options.noclion):
            output('<yellow>pass<nc>')
            return
        clionzip = 'CLion-2024.1.4.tar.gz'
        if self.install_jetbrain('CLion', clionzip, 'cpp'):
            return
        self.link_jetbrain('CLion', 'clion')
        output('- CLion installed.......: <green>Done<nc>')


    def install_webstorm(self):
        output('- install WebStorm......: ', False)
        if self.targetsys == Systems.Cygwin:
            output('<tc>not necessary<nc>')
            return
        if not flag_is_set_explicit(self.options.webstorm, self.options.nowebstorm, self.targetsys == Systems.BSD):
            output('<yellow>pass<nc>')
            return
        stormzip = 'WebStorm-2024.1.5.tar.gz'
        if self.install_jetbrain('WebStorm', stormzip, 'webstorm'):
            return
        self.link_jetbrain('WebStorm', 'webstorm')
        output('- WebStorm installed....: <green>Done<nc>')


    def install_intellij(self):
        output('- install IntelliJ......: ', False)
        if self.targetsys == Systems.Cygwin:
            output('<tc>not necessary<nc>')
            return
        if not flag_is_set_explicit(self.options.intellij, self.options.nointellij):
            output('<yellow>pass<nc>')
            return
        ideazip = 'ideaIU-2024.1.4.tar.gz'
        if self.install_jetbrain('IntelliJ', ideazip, 'idea'):
            return
        output('- IntelliJ installed.....: <green>Done<nc>')


# endregion JetBrains


    def install_code(self):
        output('- install VS Code ......: ', False)
        if self.targetsys == Systems.Cygwin or self.targetsys == Systems.Arch:
            output('<tc>not necessary<nc>')
            return
        if not flag_is_set_explicit(self.options.code, self.options.nocode, True):
            output('<yellow>pass<nc>')
            return

        code = os.popen('which code').read()[:-1]
        if "/code" in code:
            output('<yellow>Already installed<nc>')
            return

        if self.targetsys == Systems.SuSE:
            subprocess.check_call(['sudo', 'rpm', '--import', 'https://packages.microsoft.com/keys/microsoft.asc'])
            subprocess.check_call(['sudo', 'zypper', 'addrepo', 'https://packages.microsoft.com/yumrepos/vscode', 'vscode'])
            subprocess.check_call(['sudo', 'zypper', 'refresh'])
            install(self.installprog, ['code'])
        elif self.targetsys == Systems.Fedora or self.targetsys == Systems.Mageia:
            subprocess.check_call(['sudo', 'rpm', '--import', 'https://packages.microsoft.com/keys/microsoft.asc'])
            subprocess.check_call(['sudo', 'sh', '-c', 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'])
            subprocess.check_call(['sudo', 'dnf', 'check-update'])
            install(self.installprog, ['code'])
        elif self.targetsys == Systems.Ubuntu:
            path = os.getcwd()
            os.chdir(self.downloads)
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


    def install_gitflow(self):
        if self.targetsys == Systems.BSD:
            return
        if not flag_is_set_explicit(self.options.gitflow, self.options.nogitflow, True):
            output('<yellow>pass<nc>')
            return
        output('Installing git flow ....: ', False)

        flow = os.popen('which git-flow').read()[:-1]
        if "/git-flow" in flow:
            output('<yellow>Already installed<nc>')
            return

        path = os.getcwd()
        os.chdir(self.downloads)

        subprocess.check_call(['curl', '-OL', 'https://raw.github.com/nvie/gitflow/develop/contrib/gitflow-installer.sh'])
        #subprocess.call(['mkdir', 'gitflow'])
        #os.chdir('gitflow')
        subprocess.call(['git', 'clone', 'https://github.com/nvie/shFlags.git'])
        #os.chdir('..')
        subprocess.check_call(['chmod', '+x', 'gitflow-installer.sh'])
        subprocess.call(['sudo', './gitflow-installer.sh'], stdout=subprocess.PIPE)
        subprocess.call(['sudo', 'mv', 'shFlags', 'gitflow'])
        subprocess.call(['sudo', './gitflow-installer.sh'], stdout=subprocess.PIPE)
        #os.system('sudo ./gitflow-installer.sh')

        os.chdir(path)
        output('<green>Done<nc>')


    def install(self):
        output('Install externals.......: ', False)
        if self.subsys == Subsys.Windows:
            output('<tc>not necessary<nc>')
            return
        if not flag_is_set(self.options, self.options.externals, self.options.noexternals):
            output('<yellow>pass<nc>')
            return
        output('')

        self.install_gitflow()
        self.install_keybase()
        self.install_iridium()
        # self.install_brave()
        self.install_qt()
        self.install_toolbox()
        self.install_rider()
        self.install_rover()
        self.install_pycharm()
        self.install_clion()
        self.install_webstorm()
        self.install_intellij()
        self.install_code()

        output('Externals installed.....: <green>Done<nc>')
