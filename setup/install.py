# [11] Fedora             [12] FreeBSD        [13] NetBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin                  
# [  ] SuSE               [  ] Arch / Manjaro
from setup.helpers import install
from setup.console import output
from setup.dotfiles import install_dotfiles
from setup.zsh import install_zsh
from setup.prezto import install_prezto
from setup.login import install_login
from setup.fonts import install_fonts
from setup.links import install_links
from setup.xfcecfg import xfce_configure
from setup.packages import install_core, getpkgs_basics, getpkgs_programs, getpkgs_xprograms, getpkgs_compiler, \
                           getpkgs_xfce_programs, getpkgs_tex, getpkgs_games, getpkgs_nextcloud
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

    # create_ssh_key
    packages = getpkgs_basics(targetsys, subsys, options) \
        + getpkgs_programs(targetsys, subsys, options) \
        + getpkgs_xprograms(targetsys, subsys, options) \
        + getpkgs_compiler(targetsys, subsys, options) \
        + getpkgs_xfce_programs(targetsys, subsys, options) \
        + getpkgs_tex(targetsys, subsys, options) \
        + getpkgs_games(targetsys, subsys, options) \
        + getpkgs_nextcloud(targetsys, subsys, options)
    if packages:
        output('Installing programs ....: ', False)
        install(installprog, packages)
        output('<green>Done<nc>')

    xfce_configure(root, targetsys, subsys, options)
    install_dotnet(installprog, targetsys, options)
    install_externals(installprog, targetsys, subsys, options)
    clone_all(targetsys, options)
