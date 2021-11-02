import json
import os
import glob
import shutil
import sys
from pathlib import Path
from setup.osplatform import Systems, Subsys
from setup.console import output
from setup.helpers import flag_is_set

orage_id=0
weather_id = 0
eyes_id = 0
cpugraph_id = 0
netload_id = 0


terminal_launcher_id = 0
fileman_launcher_id = 0
commander_launcher_id = 0
firefox_launcher_id = 0
chrome_launcher_id = 0

# region Helpers

def get_typenames(value):
    if isinstance(value, list):
        result = '-a'
        for key in value:
            result += ' ' + get_typenames(key)
        return result
    if isinstance(value, bool):
        return '-t bool'
    if isinstance(value, int):
        return '-t int'
    if isinstance(value, float):
        return '-t double'
    return '-t string'


def get_values(value):
    if isinstance(value, list):
        result = ''
        for key in value:
            result += get_values(key) + ' '
        return result
    if isinstance(value, str):
        return '-s ' + value
    if isinstance(value, bool):
        return '-s ' + str(value).lower()
    return '-s ' + str(value)


# --- Set config value or clear it ------------------------
def call_xfconf(command, channel, prop, value):
    types = get_typenames(value)
    values = get_values(value)

    if command == 'set':
        execset = f'xfconf-query -c {channel} {types} -np {prop} {values}'
        # print (execset)
        resultset = os.popen(execset).read()
        # execRead = f'xfconf-query -c {channel} -p {property}'
        # resultRead = os.popen(execRead).read()
        # print (resultRead)
    elif command == 'clear':
        execclear = f'xfconf-query -c {channel} -p {prop} -r -R'
        resultclear = os.popen(execclear).read()
        # print (resultClear)


# --- Configure all settings ------------------------------
def configure_settings(steps):
    for step in steps:
        command = step[0]
        channel = step[1]
        keys = step[2]
        for key in keys:
            # print(f'Command {command} channel {channel} key {key}')
            value = keys[key]
            call_xfconf(command, channel, key, value)

# endregion Helpers


# region Settings

config_steps = [
    ['set', 'thunar', {
        '/default-view': 'ThunarDetailsView',
        '/last-icon-view-zoom-level': 'THUNAR_ZOOM_LEVEL_100_PERCENT',
        '/last-location-bar': 'ThunarLocationEntry',
        '/misc-date-style': 'THUNAR_DATE_STYLE_YYYYMMDD'
        }],
    ['set', 'keyboards', {
        '/Default/KeyRepeat': True,
        '/Default/KeyRepeat/Delay': 300,
        '/Default/KeyRepeat/Rate': 40
        }],
    ['set', 'xfwm4', {
        '/general/theme': 'Fbx',
        '/general/prevent_focus_stealing': True,
        '/general/workspace_count': 2,
        '/general/workspace_names': ['Work', 'Social']
        }],
    ['set', 'xfce4-session', {
        '/general/SaveOnExit': False
        }],
    ['clear', 'xfce4-keyboard-shortcuts', {
        '"/xfwm4/custom/<Alt>Insert"': None,
        '"/xfwm4/custom/<Alt>Delete"': None,
        '"/xfwm4/custom/<Shift><Alt>Page_Up"': None,
        '"/xfwm4/custom/<Shift><Alt>Page_Down"': None,
        '"/xfwm4/custom/<Primary><Alt>Up"': None,
        '"/xfwm4/custom/<Primary><Alt>Down"': None,
        '"/xfwm4/custom/<Primary><Alt>Left"': None,
        '"/xfwm4/custom/<Primary><Alt>Right"': None,
        '"/xfwm4/custom/<Primary><Alt>Home"': None,
        '"/xfwm4/custom/<Primary><Alt>End"': None,
        '"/xfwm4/custom/<Primary><Alt>KP_1"': None,
        '"/xfwm4/custom/<Primary><Alt>KP_2"': None,
        '"/xfwm4/custom/<Primary><Alt>KP_3"': None,
        '"/xfwm4/custom/<Primary><Alt>KP_4"': None,
        '"/xfwm4/custom/<Primary><Alt>KP_5"': None,
        '"/xfwm4/custom/<Primary><Alt>KP_6"': None,
        '"/xfwm4/custom/<Primary><Alt>KP_7"': None,
        '"/xfwm4/custom/<Primary><Alt>KP_8"': None,
        '"/xfwm4/custom/<Primary><Alt>KP_9"': None,
        '"/xfwm4/custom/<Primary>F3"': None,
        '"/xfwm4/custom/<Primary>F4"': None,
        '"/xfwm4/custom/<Primary>F5"': None,
        '"/xfwm4/custom/<Primary>F6"': None,
        '"/xfwm4/custom/<Primary>F7"': None,
        '"/xfwm4/custom/<Primary>F8"': None,
        '"/xfwm4/custom/<Primary>F9"': None,
        '"/xfwm4/custom/<Primary>F10"': None,
        '"/xfwm4/custom/<Primary>F11"': None,
        '"/xfwm4/custom/<Primary>F12"': None,
        }],
    ['set', 'xfce4-keyboard-shortcuts', {
        '"/xfwm4/custom/<Super>d"': 'show_desktop_key',
        '"/xfwm4/custom/<Super>Up"': 'maximize_window_key',
        '"/xfwm4/custom/<Super>Left"': 'tile_left_key',
        '"/xfwm4/custom/<Super>Right"': 'tile_right_key',
        '"/xfwm4/custom/<Super>Home"': 'tile_up_left_key',
        '"/xfwm4/custom/<Super>End"': 'tile_down_left_key',
        '"/xfwm4/custom/<Super>Page_Up"': 'tile_up_right_key',
        '"/xfwm4/custom/<Super>Page_Down"': 'tile_down_right_key',
        '"/xfwm4/custom/<Alt><Super>Left"': 'workspace_1_key',
        '"/xfwm4/custom/<Alt><Super>Right"': 'workspace_2_key',
        '"/xfwm4/custom/<Shift><Super>Left"': 'move_window_workspace_1_key',
        '"/xfwm4/custom/<Shift><Super>Right"': 'move_window_workspace_2_key',
        }],
    ['clear', 'xfce4-panel', {
        '/panels': None,
        '/plugins': None
        }],
]

# endregion Settings


# region Plugins

def get_menu_plugin(current, plugins, targetsys):
    icon = 'xfce4-panel-menu' if targetsys != Systems.BSD else 'org.xfce.panel.applicationsmenu'
    plugins.update({
        f'/plugins/plugin-{current}': 'applicationsmenu',
        f'/plugins/plugin-{current}/button-icon': icon,
        f'/plugins/plugin-{current}/button-title': 'Menu',
        f'/plugins/plugin-{current}/show-button-title': False,
        f'/plugins/plugin-{current}/show-menu-icons': True,
        f'/plugins/plugin-{current}/show-tooltips': False,
    })
    return current+1


def get_tasklist_plugin(current, plugins):
    plugins.update({
        f'/plugins/plugin-{current}': 'tasklist',
        f'/plugins/plugin-{current}/flat-buttons': True,
        f'/plugins/plugin-{current}/grouping': 1,
        f'/plugins/plugin-{current}/show-handle': True,
        f'/plugins/plugin-{current}/show-wireframes': False,
        f'/plugins/plugin-{current}/window-scrolling': False,
        f'/plugins/plugin-{current}/include-all-workspaces': False,
    })
    return current+1


def get_separator_plugin(current, plugins):
    plugins.update({
        f'/plugins/plugin-{current}': 'separator',
        f'/plugins/plugin-{current}/expand': True,
        f'/plugins/plugin-{current}/style': 0,
    })
    return current+1


def get_pager_plugin(current, plugins):
    plugins.update({
        f'/plugins/plugin-{current}': 'pager',
        f'/plugins/plugin-{current}/miniature-view': True,
        f'/plugins/plugin-{current}/rows': 1,
        f'/plugins/plugin-{current}/workspace-scrolling': False,
    })
    return current+1


def add_eyes_plugin(current, plugins, targetsys):
    eyes_id = current
    if targetsys != Systems.BSD:
        plugins.update({f'/plugins/plugin-{current}': 'eyes'})
        return current + 1
    return current
def add_screenshot_plugin(current, plugins):
    plugins.update({f'/plugins/plugin-{current}': 'screenshooter'})
    return current + 1
def add_weather_plugin(current, plugins):
    global weather_id
    weather_id = current
    plugins.update({
        f'/plugins/plugin-{current}': 'weather',
        f'/plugins/plugin-{current}/timezone': 'Europe/Berlin',
        f'/plugins/plugin-{current}/location/name': 'Brebach, Neufechingen',
        f'/plugins/plugin-{current}/location/latitude': '49.212737',
        f'/plugins/plugin-{current}/location/longitude': '7.037100',
    })
    return current + 1
def add_cpugraph_plugin(current, plugins):
    global cpugraph_id
    cpugraph_id = current
    plugins.update({f'/plugins/plugin-{current}': 'cpugraph'})
    return current + 1
def get_before_systray_plugin(current, plugins, targetsys):
    current = add_eyes_plugin(current, plugins, targetsys)
    current = add_screenshot_plugin(current, plugins)
    current = add_weather_plugin(current, plugins)
    #    '/plugins/plugin-9': 'xfce-clipman-plugin',  # Zwischenablage
    #    '/plugins/plugin-10': 'xkb',  # Tastatursprache
    current = add_cpugraph_plugin(current, plugins)
    #    '/plugins/plugin-12': 'netload',  # Netzauslastung
    return current


def get_systray_plugin(current, plugins, targetsys):
    ordered = ['Keybase']
    if targetsys == Systems.Fedora:
        ordered += 'dnfdragora-updater'
    legacy = ['hexchat', 'nextcloud', 'ibus panel']
    plugins.update({
        f'/plugins/plugin-{current}': 'systray',  # Externe Elemente
        # f'/plugins/plugin-{current}/names-hidden': [],
        f'/plugins/plugin-{current}/show-frame': False,
        f'/plugins/plugin-{current}/size-max': 22,
        f'/plugins/plugin-{current}/square-icons': True,
        f'/plugins/plugin-{current}/names-ordered': ordered,
        f'/plugins/plugin-{current}/known-legacy_items': legacy,
    })
    return current + 1


def add_powerman_plugin(current, plugins):
    plugins.update({f'/plugins/plugin-{current}': 'power-manager-plugin'})
    return current + 1
def add_notification_plugin(current, plugins):
    plugins.update({f'/plugins/plugin-{current}': 'notification-plugin'})
    return current + 1
def add_pulseaudio_plugin(current, plugins):
    plugins.update({
        f'/plugins/plugin-{current}': 'pulseaudio',
        f'/plugins/plugin-{current}/enable-keyboard-shortcuts': True,
        f'/plugins/plugin-{current}/show-notifications': True,
    })
    return current + 1
def add_clock_plugin(current, plugins):
    plugins.update({
        f'/plugins/plugin-{current}': 'clock',
        f'/plugins/plugin-{current}/digital-format': '%_H:%M',
    })
    return current + 1
def add_actions_plugin(current, plugins):
    plugins.update({
        f'/plugins/plugin-{current}': 'actions',
        f'/plugins/plugin-{current}/appearance': 1,
        f'/plugins/plugin-{current}/ask-confirmation': True,
    })
    return current + 1
def get_after_systray_plugin(current, plugins, targetsys):
    current = add_powerman_plugin(current, plugins)
    current = add_notification_plugin(current, plugins)
    current = add_pulseaudio_plugin(current, plugins)
    current = add_clock_plugin(current, plugins)
    current = add_actions_plugin(current, plugins)
    return current


def add_terminal_launcher(current, plugins):
    plugins.update({
        f'/plugins/plugin-{current}': 'launcher',
        f'/plugins/plugin-{current}/items': ['exo-terminal-emulator.desktop'],
    })
    return True
def add_fileman_launcher(current, plugins):
    plugins.update({
        f'/plugins/plugin-{current}': 'launcher',
        f'/plugins/plugin-{current}/items': ['exo-file-manager.desktop'],
    })
    return True
def add_commander_launcher(current, plugins, targetsys):
    if targetsys != Systems.BSD:
        plugins.update({
            f'/plugins/plugin-{current}': 'launcher',
            f'/plugins/plugin-{current}/items': ['exo-file-commander.desktop'],
        })
        return True
    return False
def add_firefox_launcher(current, plugins):
    plugins.update({
        f'/plugins/plugin-{current}': 'launcher',
        f'/plugins/plugin-{current}/items': ['exo-firefox.desktop'],
    })
    return True
def add_chrome_launcher(current, plugins):
    plugins.update({
        f'/plugins/plugin-{current}': 'launcher',
        f'/plugins/plugin-{current}/items': ['exo-chromium.desktop'],
    })
    return True


def add_launchers(current, plugins, targetsys):
    launchers = []
    if add_terminal_launcher(current, plugins):
        global terminal_launcher_id
        terminal_launcher_id = current
        launchers.append(terminal_launcher_id)
    current += 1
    if add_fileman_launcher(current, plugins):
        global fileman_launcher_id
        fileman_launcher_id = current
        launchers.append(fileman_launcher_id)
    current += 1
    if add_commander_launcher(current, plugins, targetsys):
        global commander_launcher_id
        commander_launcher_id = current
        launchers.append(commander_launcher_id)
    current += 1
    if add_firefox_launcher(current, plugins):
        global firefox_launcher_id
        firefox_launcher_id = current
        launchers.append(firefox_launcher_id)
    current += 1
    if add_chrome_launcher(current, plugins):
        global chrome_launcher_id
        chrome_launcher_id = current
        launchers.append(chrome_launcher_id)
    return launchers


def add_panel(plugins, pluginlist):
    plugins.update({
        '/panels/panel-1/autohide-behavior': 0,
        # '/panels/panel-1/background-style': 1,
        # '/panels/panel-1/background-alpha': 100,
        # '/panels/panel-1/background-rgba': [0.596078, 0.415686, 0.266667, 1.000000],
        '/panels/panel-1/disable-struts': False,
        '/panels/panel-1/enter-opacity': 100,
        '/panels/panel-1/leave-opacity': 100,
        '/panels/panel-1/length': 100,
        '/panels/panel-1/mode': 0,
        '/panels/panel-1/nrows': 1,
        '/panels/panel-1/plugin-ids': pluginlist,
        '/panels/panel-1/position': 'p=6\;x=0\;y=0',
        '/panels/panel-1/position-locked': True,
        '/panels/panel-1/size': 24,
        '/panels/dark-mode': True,
        '/panels': [1],
    })


def get_plugin_settings(targetsys):
    plugins = {}
    current = 1
    current = get_menu_plugin(current, plugins, targetsys)
    current = get_tasklist_plugin(current, plugins)
    current = get_separator_plugin(current, plugins)
    current = get_pager_plugin(current, plugins)
    current = get_before_systray_plugin(current, plugins, targetsys)
    current = get_systray_plugin(current, plugins, targetsys)
    current = get_after_systray_plugin(current, plugins, targetsys)

    plugin_list = [1]
    for item in add_launchers(current, plugins, targetsys):
        if item > 0:
            plugin_list.append(item)
    for plug in range(2, current):
        plugin_list.append(plug)
    add_panel(plugins, plugin_list)
    return [['set', 'xfce4-panel', plugins]]

# endregion Plugins


# region Links and Commands

def link_xfce_file(root, filename, target_id, folder=''):
    source = f'{root}/etc/unix/xfce4/{filename}.rc'
    target = str(Path.home()) + '/.config/xfce4/'
    if folder:
        target = target + folder + '/'
    target += f'{filename}-{target_id}.rc'

    if os.path.islink(target):
        return
    if os.path.isfile(target):
        os.rename(target, target + '.bak')
    os.symlink(source, target)


def clear_xfce_launchers():
    targets = str(Path.home()) + '/.config/xfce4/panel/launcher-*'
    launchers = glob.glob(targets)
    for launcher in launchers:
        shutil.rmtree(launcher)


def copy_xfce_launcher(root, filename, id):
    source = root + '/etc/unix/xfce4/' + filename
    target = str(Path.home()) + '/.config/xfce4/panel/launcher-' + str(id)
    if not os.path.isdir(target):
        os.mkdir(target)
    target += '/' + filename
    if os.path.islink(target):
        return
    shutil.copy(source, target)


def install_links(root):
    xfce_source = root + '/etc/unix/xfce4/'
    xfce_path = str(Path.home()) + '/.config/xfce4/'
    xfce_panel = 'panel/'
    # xfceChannel = 'xfconf/xfce-perchannel-xml/'
    global orage_id
    if orage_id > 0:
        link_xfce_file(root, 'xfce4-orageclock-plugin', orage_id, xfce_panel)
    global weather_id
    if weather_id > 0:
        link_xfce_file(root, 'weather', weather_id, xfce_panel)
    global eyes_id
    if eyes_id > 0:
        link_xfce_file(root, 'eyes', eyes_id, xfce_panel)
    global cpugraph_id
    if cpugraph_id > 0:
        link_xfce_file(root, 'cpugraph', cpugraph_id, xfce_panel)
    global netload_id
    if netload_id > 0:
        link_xfce_file(root, 'netload', netload_id, xfce_panel)

    clear_xfce_launchers()

    global terminal_launcher_id
    if terminal_launcher_id > 0:
        copy_xfce_launcher(root, 'exo-terminal-emulator.desktop', terminal_launcher_id)
    # copy_xfce_launcher(root, 'exo-terminal-byobu.desktop', 20)
    global fileman_launcher_id
    if fileman_launcher_id > 0:
        copy_xfce_launcher(root, 'exo-file-manager.desktop', fileman_launcher_id)
    global commander_launcher_id
    if commander_launcher_id > 0:
        copy_xfce_launcher(root, 'exo-file-commander.desktop', commander_launcher_id)
    global firefox_launcher_id
    if firefox_launcher_id > 0:
        copy_xfce_launcher(root, 'exo-firefox.desktop', firefox_launcher_id)
    global chrome_launcher_id
    if chrome_launcher_id > 0:
        copy_xfce_launcher(root, 'exo-chromium.desktop', chrome_launcher_id)

# endregion Links and Commands


#  region Debug query

# --- List plugins ----------------------------------------
def read_plugins():
    # https://docs.xfce.org/xfce/xfconf/xfconf-query
    plugins_read = 'xfconf-query -c xfce4-panel -p /plugins -l'
    plugins = os.popen(plugins_read).read().splitlines()
    for plugin in plugins:
        index = len('/plugins/plugin-')
        tmp = plugin[index::]
        if '/' in tmp:
            continue

        plugin_id = int(tmp)
        name_plugin = f'xfconf-query -c xfce4-panel -p /plugins/plugin-{plugin_id}'
        plugin_name = os.popen(name_plugin).read().splitlines()[0]

        print(f'Plugin {plugin_id} is {plugin_name}')

#  endregion Debug query


# [11] Fedora             [12] FreeBSD
# [05] Xubuntu            [  ] MX
# [02] Ubuntu on Windows  [03] Cygwin
# [  ] SuSE               [  ] Arch / Manjaro
def xfce_configure(root, targetsys, subsys, options):
    # read_plugins()
    output('Configure XFCE..........: ', False)
    if targetsys == Systems.Cygwin or subsys == Subsys.Windows:
        output('<tc>not necessary<nc>')
        return
    if not flag_is_set(options, options.xfcecfg, options.noxfcecfg):
        output('<yellow>pass<nc>')
        return
    #configure_settings(config_steps)

    plugins = get_plugin_settings(targetsys)
    #json.dump(plugins, sys.stdout)
    configure_settings(plugins)

    install_links(root)
    output('<green>Ok<nc>')
