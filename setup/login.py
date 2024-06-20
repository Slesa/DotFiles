# [11] Fedora             [15] RHEL/Alma       [14] SuSE
# [12] FreeBSD            [13] NetBSD
# [05] Xubuntu            [  ] MX              [16] Mageia
# [02] Ubuntu on Windows  [03] Cygwin          [  ] Arch / Manjaro
import os
import subprocess
from setup.osplatform import Systems, Subsys
from setup.console import output
from setup.helpers import flag_is_set


def install_login(root, targetsys, subsys, options):
    output('Install Login...........: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return
    if not options.desktop == 'xfce':
        output('<yellow>XFCE not used<nc>')
        return
    #if targetsys == Systems.BSD or targetsys == Systems.NetBSD:
    #    output('<yellow>uses SLIM<nc>')
    #    return
    if not flag_is_set(options, options.login, options.nologin):
        output('<yellow>pass<nc>')
        return
    configfile = '/etc/lightdm/lightdm-gtk-greeter.conf'
    if targetsys == Systems.BSD or targetsys == Systems.NetBSD:
        targetdir = '/usr/local/share/pixmaps/'
        configfile = '/usr/local/etc/lightdm/lightdm-gtk-greeter.conf'
    elif targetsys == Systems.SuSE:
        targetdir = '/usr/share/wallpapers/'
    else:
        targetdir = '/usr/share/backgrounds/'
    targetfile = 'StarTrekLogo1920x1080.jpg'
    # elif targetsys == Systems.Fedora or targetsys == Systems.MxLinux:
    #    targetdir = '/usr/share/backgrounds/'
    # elif targetsys == Systems.BSD:
    #    targetdir = '/usr/local/share/backgrounds/'
    #    configfile = '/usr/local/share/PCDM/themes/trueos/trueos.theme'
    if not os.path.isfile(targetdir + targetfile):
        subprocess.check_call(['sudo', 'cp', root + '/data/img/' + targetfile, targetdir + targetfile])
        subprocess.check_call(['sudo', 'chmod', '+r', targetdir + targetfile])
    if options.desktop == 'xfce':
        r1 = subprocess.run(
            ['sudo', 'sed', '-i', '-e', f's#[#^]background=.*#background={targetdir}{targetfile}#g', configfile])
        # print(r1)
        r2 = subprocess.run(['sudo', 'sed', '-i', '-e', 's/\#theme-name=/theme-name=Ambience/g', configfile])
        # print(r2)

    output('<green>Ok<nc>')
