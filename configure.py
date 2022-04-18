# [11] Fedora             [12] FreeBSD        [13] NetBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin                  
# [14] SuSE               [  ] Arch / Manjaro
import os
from pathlib import Path
from setup.console import output
from setup.parser import create_parser
from setup.osplatform import determine_os, determine_installer
from setup.install import install_all


# Renoise, mp3 (-verwaltung), GitKraken?, XMind

output("<head>=====[ Configuring system ]====<nc>")
(system,subsys) = determine_os()
if system is None:
    quit()
installer = determine_installer(system)
args = create_parser()

#output(f'Systems is <green>{system}<nc> with installer <tc>{installer}<nc>')
#copy_text_to_clipboard(system, 'This is a test clip')
#ensure_root(system)
basepath = str(Path.home()) + '/.dotfiles'
install_all(basepath, system, subsys, installer, args)
