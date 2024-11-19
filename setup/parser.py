# [11] Fedora             [15] RHEL/Alma       [14] SuSE
# [12] FreeBSD            [13] NetBSD
# [05] Xubuntu            [  ] MX              [16] Mageia
# [02] Ubuntu on Windows  [03] Cygwin          [  ] Arch / Manjaro
import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-desktop', default='xfce', choices=['xfce', 'kde', 'gnome', 'i3wm'])
    parser.add_argument('-full', action='store_true')
    parser.add_argument('-zsh', action='store_true')
    parser.add_argument('-nozsh', action='store_true')
    parser.add_argument('-prezto', action='store_true')
    parser.add_argument('-noprezto', action='store_true')
    parser.add_argument('-login', action='store_true')
    parser.add_argument('-nologin', action='store_true')
    parser.add_argument('-links', action='store_true')
    parser.add_argument('-nolinks', action='store_true')
    parser.add_argument('-core', action='store_true')
    parser.add_argument('-nocore', action='store_true')
    parser.add_argument('-nextcloud', action='store_true')
    parser.add_argument('-nonextcloud', action='store_true')
    parser.add_argument('-dotfiles', action='store_true')
    parser.add_argument('-nodotfiles', action='store_true')
    parser.add_argument('-basics', action='store_true')
    parser.add_argument('-nobasics', action='store_true')
    parser.add_argument('-programs', action='store_true')
    parser.add_argument('-noprograms', action='store_true')
    parser.add_argument('-xprograms', action='store_true')
    parser.add_argument('--noxprograms', action='store_true')
    parser.add_argument('-compiler', action='store_true')
    parser.add_argument('-nocompiler', action='store_true')
    parser.add_argument('-i3wm', action='store_true')
    parser.add_argument('-noi3wm', action='store_true')
    parser.add_argument('-xfce', action='store_true')
    parser.add_argument('-noxfce', action='store_true')
    parser.add_argument('-xfcecfg', action='store_true')
    parser.add_argument('-noxfcecfg', action='store_true')
    parser.add_argument('-tex', action='store_true')
    parser.add_argument('-notex', action='store_true')
    parser.add_argument('-games', action='store_true')
    parser.add_argument('-nogames', action='store_true')
    parser.add_argument('-fonts', action='store_true')
    parser.add_argument('-nofonts', action='store_true')
    parser.add_argument('-clone', action='store_true')
    parser.add_argument('-noclone', action='store_true')
    parser.add_argument('-bitbucket', action='store_true')
    parser.add_argument('-nobitbucket', action='store_true')
    parser.add_argument('-github', action='store_true')
    parser.add_argument('-nogithub', action='store_true')
    parser.add_argument('-gitlab', action='store_true')
    parser.add_argument('-nogitlab', action='store_true')
    parser.add_argument('-gf', action='store_true')
    parser.add_argument('-nogf', action='store_true')
    parser.add_argument('-externals', action='store_true')
    parser.add_argument('-noexternals', action='store_true')
    parser.add_argument('-keybase', action='store_true')
    parser.add_argument('-nokeybase', action='store_true')
    #parser.add_argument('-brave', action='store_true')
    #parser.add_argument('-nobrave', action='store_true')
    parser.add_argument('-iridium', action='store_true')
    parser.add_argument('-noiridium', action='store_true')
    parser.add_argument('-qt', action='store_true')
    parser.add_argument('-noqt', action='store_true')
    parser.add_argument('-toolbox', action='store_true')
    parser.add_argument('-notoolbox', action='store_true')
    parser.add_argument('-rider', action='store_true')
    parser.add_argument('-norider', action='store_true')
    parser.add_argument('-rover', action='store_true')
    parser.add_argument('-norover', action='store_true')
    parser.add_argument('-pycharm', action='store_true')
    parser.add_argument('-nopycharm', action='store_true')
    parser.add_argument('-clion', action='store_true')
    parser.add_argument('-noclion', action='store_true')
    parser.add_argument('-webstorm', action='store_true')
    parser.add_argument('-nowebstorm', action='store_true')
    parser.add_argument('-intellij', action='store_true')
    parser.add_argument('-nointellij', action='store_true')
    parser.add_argument('-code', action='store_true')
    parser.add_argument('-nocode', action='store_true')
    parser.add_argument('-dotnet', action='store_true')
    parser.add_argument('-nodotnet', action='store_true')
    parser.add_argument('-gitflow', action='store_true')
    parser.add_argument('-nogitflow', action='store_true')
    result = parser.parse_args()
    return result

