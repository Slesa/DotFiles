# [11] Fedora             [15] RHEL/Alma       [14] SuSE
# [12] FreeBSD            [13] NetBSD
# [05] Xubuntu            [  ] MX              [16] Mageia
# [02] Ubuntu on Windows  [03] Cygwin          [  ] Arch / Manjaro
from setup.helpers import install
from setup.console import output
from setup.dotfiles import install_dotfiles
from setup.zsh import install_zsh
from setup.prezto import install_prezto
from setup.login import install_login
from setup.fonts import install_fonts
from setup.links import install_links
from setup.xfcecfg import xfce_configure
from setup.packages import install_core, Installer
from setup.cloning import clone_all
from setup.dotnet import install_dotnet
from setup.externals import install_externals


def install_all(root, targetsys, subsys, installprog, options):
    install_core(installprog, targetsys, subsys, options)
    install_dotfiles(root, options)
    install_zsh(root, targetsys, options)
    install_prezto(targetsys, options)
    install_login(root, targetsys, subsys, options)
    install_fonts(root, targetsys, subsys, options)
    install_links(root, targetsys, subsys, options)

    installer = Installer(targetsys, subsys, options)
    # create_ssh_key
    packages = installer.getpkgs_basics() \
        + installer.getpkgs_programs() \
        + installer.getpkgs_xprograms() \
        + installer.getpkgs_compiler() \
        + installer.getpkgs_xfce_programs() \
        + installer.getpkgs_tex() \
        + installer.getpkgs_games() \
        + installer.getpkgs_nextcloud()
    if packages:
        output('Installing programs ....: ', False)
        install(installprog, packages)
        output('<green>Done<nc>')

    xfce_configure(root, targetsys, subsys, options)
    install_dotnet(installprog, targetsys, options)
    install_externals(installprog, targetsys, subsys, options)
    clone_all(targetsys, options)
