# [11] Fedora             [15] RHEL/Alma       [14] SuSE
# [12] FreeBSD            [13] NetBSD
# [05] Xubuntu            [  ] MX              [16] Mageia
# [02] Ubuntu on Windows  [03] Cygwin          [  ] Arch / Manjaro
import os
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
    Redhat = 9
    Mageia = 10
    BSD = 11
    NetBSD = 12
    SunOS = 13


class Subsys(Enum):
    Origin = 0
    Windows = 1


def determine_os():
    output(f'System..................: <green>{platform.system()}<nc>')
        
    release = platform.release().lower()
    subsys = Subsys.Windows if 'microsoft' in release else Subsys.Origin
    output('Found...................: ', False)
    system = platform.system().lower()
    if system.startswith('cygwin'):
        output('<green>CygWin<nc>')
        return Systems.Cygwin, subsys
    if system == 'darwin':
        output('<green>MacOS<nc>')
        return Systems.MacOS, subsys
    if system == 'netbsd':
        output('<green>NetBSD<nc>')
        return Systems.NetBSD, subsys
    if system == 'sunos':
        output('<green>Sun OS<nc>')
        return Systems.SunOS, subsys
    if 'bsd' in system:
        output('<green>BSD derivate<nc>')
        return Systems.BSD, subsys
    if system == 'linux':
        linux = platform.platform().lower() + platform.version().lower()
        if '.fc3' in linux:
            output('<green>Fedora<nc>')
            return Systems.Fedora, subsys
        if '.mga' in linux:
            output('<green>Mageia<nc>')
            return Systems.Mageia, subsys
        if 'mx' in linux:
            output('<green>MXLinux<nc>')
            return Systems.MxLinux, subsys
        if 'alma' in linux:
            output('<green>Redhat<nc>')
            return Systems.Redhat, subsys
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

    flow = os.popen('which zypper').read()[:-1]
    if '/zypper' in flow:
        output('<green>SuSE<nc>')
        return Systems.SuSE, subsys
    
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
    if os == Systems.SunOS:
        return ["sudo", "pkg", "install", "--accept"]
    if os == Systems.NetBSD:
        return ["sudo", "pkgin", "-y", "install"]
    if os == Systems.Mageia:
        return ["sudo", "dnf", "install", "-y"]
    if os == Systems.Fedora:
        return ["sudo", "dnf", "install", "-y"]
    if os == Systems.Redhat:
        return ["sudo", "dnf", "install", "-y"]
    if os == Systems.MxLinux:
        return ["sudo", "apt-get", "install", "-y"]
    if os == Systems.SuSE:
        return ["sudo", "zypper", "install", "-ly"]
    if os == Systems.Arch:
        return ["sudo", "pacman", "--noconfirm", "-Syu"]
    if os == Systems.Ubuntu or os == Systems.Zorin:
        return ["sudo", "apt-get", "install", "-y"]
    if os == Systems.MacOS:
        return ["sudo", "brew", "install", "-y"]
    return None
