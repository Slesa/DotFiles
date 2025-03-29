# [11] Fedora       [12] FreeBSD     [  ] Arch/Manjaro   [14] SuSE Tumbleweed
# [02] Ubuntu WSL   [03] Cygwin      [  ] MX             [16] Mageia
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
    Arch = 6 # Manjaro
    Ubuntu = 7
    Zorin = 8
    Redhat = 9
    Mageia = 10
    FreeBSD = 11
    NetBSD = 12
    OpenBSD = 13
    SunOS = 14
    Raspbian = 15
    Debian = 16


class Subsys(Enum):
    Origin = 0
    Windows = 1


def os_from_line(line):
    if 'debian' in line:
        if os.path.isfile('/etc/mx-version'):
            output('<green>MX Linux<nc>')
            return Systems.MxLinux;
        else:
            output('<green>Debian<nc>')
            return Systems.Debian;
    if 'fedora' in line:
        output('<green>Fedora<nc>')
        return Systems.Fedora
    if 'ubuntu' in line:
        output('<green>Ubuntu<nc>')
        return Systems.Ubuntu
    if 'arch' in line or 'manjaro' in line:
        output('<green>Arch / Manjaro<nc>')
        return Systems.Arch
    if 'raspbian' in line:
        output('<green>Raspbian<nc>')
        return Systems.Raspbian
    return None


def read_osinfo():
    if not os.path.exists('/etc/os-release'):
        return None
    with open('/etc/os-release') as fh:
        lines = fh.readlines()
        for line in lines:
            content = line.lower()
            if 'pretty_name' in content:
                return os_from_line(content)
    return None


def determine_os():
    output(f'System..................: <green>{platform.system()}<nc>')

    release = platform.release().lower()
    subsys = Subsys.Windows if 'wsl2' in release else Subsys.Origin

    output('Found...................: ', False)
    osinfo = read_osinfo()
    #output(f'Pretty name.............: <green>{osinfo}<nc>')
        
    if subsys == Subsys.Windows:
        output('<yellow>Detected WSL<nc>') 
    #    distro = os.environ['WSL_DISTRO_NAME'].lower()
    #    if distro == 'ubuntu':
    #        output(f'<green>WSL Ubuntu {subsys}<nc>')
    #        return Systems.Ubuntu, subsys
    if osinfo!=None:
        return osinfo, subsys

    system = platform.system().lower()
    if system.startswith('cygwin'):
        output('<green>CygWin<nc>')
        return Systems.Cygwin, subsys
    if system == 'darwin':
        output('<green>MacOS<nc>')
        return Systems.MacOS, subsys
    if system == 'openbsd':
        output('<green>OpenBSD<nc>')
        return Systems.OpenBSD, subsys
    if system == 'netbsd':
        output('<green>NetBSD<nc>')
        return Systems.NetBSD, subsys
    if system == 'sunos':
        output('<green>Sun OS<nc>')
        return Systems.SunOS, subsys
    if 'freebsd' in system:
        output('<green>FreeBSD<nc>')
        return Systems.FreeBSD, subsys
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
    if os == Systems.FreeBSD:
        return ["sudo", "pkg", "install", "-y"]
    if os == Systems.SunOS:
        return ["sudo", "pkg", "install", "--accept"]
    if os == Systems.NetBSD:
        return ["sudo", "pkgin", "-y", "install"]
    if os == Systems.OpenBSD:
        return ["doas", "pkg_add", "-i"]
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
    if os == Systems.Debian or os == Systems.Ubuntu or os == Systems.Zorin or os == Systems.Raspbian:
        return ["sudo", "apt-get", "install", "-y"]
    if os == Systems.MacOS:
        return ["sudo", "brew", "install", "-y"]
    return None
