import os
from setup.osplatform import Systems, Subsys
from setup.console import output
from setup.helpers import flag_is_set, get_downloads, install


# [13] Fedora             [12] FreeBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin
# [  ] SuSE               [  ] Arch / Manjaro
def install_dotnet(installprog, targetsys, options):
    output('install .NET Core ......: ', False)
    if targetsys == Systems.Cygwin:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.dotnet, options.nodotnet):
        output('<yellow>pass<nc>')
        return
    path = os.getcwd()
    os.chdir('/tmp')

    packages = ['dotnet-sdk-5.0', 'aspnetcore-runtime-5.0', 'dotnet-runtime-5.0', 'dotnet-templates-5.0']
    # packages = ['dotnet-sdk-5.0', 'aspnetcore-runtime-5.0', 'dotnet-sdk-3.1', 'aspnetcore-runtime-3.1', 'dotnet-runtime-3.1']
    # packages = ['dotnet-sdk-3.1', 'aspnetcore-runtime-3.1', 'dotnet-runtime-3.1']

    if targetsys == Systems.BSD:
        packages = ['linux-dotnet10-sdk', 'linux-dotnet10-runtime']
    elif targetsys == Systems.Ubuntu or targetsys == Systems.Zorin or targetsys == Systems.MxLinux:
        os.popen('wget https://packages.microsoft.com/config/ubuntu/20.10/packages-microsoft-prod.deb -O packages-microsoft-prod.deb')
        os.popen('sudo dpkg -i packages-microsoft-prod.deb')
    elif targetsys == Systems.SuSE:
        os.popen('sudo zypper install libicu')
        os.popen('sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc')
        os.popen('wget https://packages.microsoft.com/config/opensuse/15/prod.repo')
        os.popen('sudo mv prod.repo /etc/zypp/repos.d/microsoft-prod.repo')
        os.popen('sudo chown root:root /etc/zypp/repos.d/microsoft-prod.repo')
    elif targetsys == Systems.Arch:
        output('<red>unsupported<nc>')
    elif targetsys == Systems.Fedora:
        os.popen('sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc')
        os.popen('sudo wget -O /etc/yum.repos.d/microsoft-prod.repo https://packages.microsoft.com/config/fedora/33/prod.repo')
        os.popen('sudo dnf check-update')
        os.popen('sudo dnf update')
    os.chdir(path)

    install(installprog, packages)
    output('<green>Ok<nc>')

