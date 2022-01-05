# [11] Fedora             [12] FreeBSD        [13] NetBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin                  
# [  ] SuSE               [  ] Arch / Manjaro
import platform
from enum import Enum
from setup.console import output


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


class Systems(Enum):
    Unknown = 0
    Cygwin = 1
    MacOS = 2
    MxLinux = 3
    Fedora = 4
    SuSE = 5
    Arch = 6
    Ubuntu = 7
    Zorin = 8
    BSD = 11
    NetBSD = 12


class Subsys(Enum):
    Origin = 0
    Windows = 1


def determine_os():
    output(f'System..................: <green>{platform.system()}<nc>')
    # [0.3] cygwin                  [0.A] Debian
    # [ ] macos                     [ ] SuSE
    # [0.C] FreeBSD                 [ ] Arch / Manjaro
    # [0.2] Ubuntu on Windows       [0.5] Ubuntu
    # [ ] Fedora                    [0.7] Zorin
    
    release = platform.release().lower()
    subsys = Subsys.Windows if 'microsoft' in release else Subsys.Origin
    output('Found...................: ', False)
    system = platform.system().lower()
    if system.startswith('cygwin'):
        output('<green>CygWin<nc>')
        return Systems.Cygwin, subsys
    if system == 'darwin':
        output('<green>MacOS<nc>')
        return Systems.MacOs, subsys
    if system == 'netbsd':
        output('<green>NetBSD<nc>')
        return Systems.NetBSD, subsys
    if 'bsd' in system:
        output('<green>BSD derivate<nc>')
        return Systems.BSD, subsys
    if system == 'linux':
        linux = platform.platform().lower() + platform.version().lower()
        if '.fc3' in linux:
            output('<green>Fedora<nc>')
            return Systems.Fedora, subsys
        if 'mx' in linux:
            output('<green>MXLinux<nc>')
            return Systems.MxLinux, subsys
        if 'suse' in linux:
            output('<green>SuSE<nc>')
            return Systems.SuSE, subsys
        if 'arch' in linux or 'manjaro' in linux:
            output('<green>Arch / Manjaro<nc>')
            return Systems.Arch, subsys
        if 'ubuntu' in linux:
            output(f'<green>Ubuntu {subsys}<nc>')
            return Systems.Ubuntu, subsys
        if 'zorin' in linux:
            output(f'<green>Zorin {subsys}<nc>')
            return Systems.Zorin, subsys
    output('<red>Unknown<nc>')
    output(f'Platform................: <yellow>{platform.platform()}<nc>')
    output(f'Release.................: <yellow>{platform.release()}<nc>')
    output(f'Version.................: <yellow>{platform.version()}<nc>')
    # output(f'Uname...................: <yellow>{str(platform.uname())}<nc>')
    # output(f'Distribution............: <yellow>{platform.linux_distribution()[0]}<nc>')
    return None, subsys


def determine_installer(os):
    if os == Systems.BSD:
        return ["sudo", "pkg", "install", "-y"]
    if os == Systems.NetBSD:
        return ["sudo", "pkgin", "-y", "install"]
    if os == Systems.Fedora:
        return ["sudo", "dnf", "install", "-y"]
    if os == Systems.MxLinux:
        return ["sudo", "apt-get", "install", "-y"]
    if os == Systems.SuSE:
        return ["sudo", "zypper", "install", "-ly"]
    if os == Systems.Arch:
        return ["sudo", "pacman", "--noconfirm", "-Syu"]
    if os == Systems.Ubuntu or os == Systems.Zorin:
        return ["sudo", "apt-get", "install", "-y"]
    return None
