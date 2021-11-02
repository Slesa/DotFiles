import os
import subprocess
from pathlib import Path
from setup.osplatform import Systems, Subsys
from setup.console import output
from setup.helpers import flag_is_set


# [11] Fedora             [12] FreeBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin
# [  ] SuSE               [  ] Arch / Manjaro
def install_fonts(root, targetsys, subsys, options):
    output('Install Fonts...........: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.fonts, options.nofonts):
        output('<yellow>pass<nc>')
        return
    targetdir = '/usr/share/fonts' if not targetsys == Systems.BSD else '/usr/local/share/fonts/TTF'
    # envyfonts = Path(targetdir).glob('*.ttf')
    targetfont = Path(Path(targetdir) / 'Envy Code R.ttf')
    if os.path.isfile(targetfont):
        output('<green>already installed<nc>')
    else:
        output('<tc>copying<nc>')
        fonts = Path(root + '/data/font').glob('*.ttf')
        for font in fonts:
            subprocess.check_call(['sudo', 'cp', str(font), targetdir])
        # subprocess.check_call(['sudo', 'cp', '"' + Basepath + '/data/font/*"', targetdir])
        devnull = open(os.devnull, 'w')
        subprocess.check_call(['sudo', 'fc-cache', '-fv'], stdout=devnull)
        output('Fonts installed.........: <green>Done<nc>')
