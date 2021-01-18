import os
import subprocess

# https://docs.xfce.org/xfce/xfconf/xfconf-query

#region Output

Colors = [
    ('<red>', '\033[0;31m'),
    ('<green>', '\033[0;32m'),
    ('<yellow>', '\033[0;33m'),
    ('<head>', '\033[0;35m'),
    ('<tc>', '\033[0;33m'),
    ('<nc>', '\033[0m')]

def output(msg, cr=True):
    buffer = msg
    for idx,col in enumerate(Colors):
        buffer = buffer.replace(col[0], col[1])
    if cr:
        print(buffer)
    else:
        print(buffer, end='')

#endregion

config_steps = [
  [ 'set', 'thunar', {
      '/default-view': 'ThunarDetailsView',
      '/last-icon-view-zoom-level': 'THUNAR_ZOOM_LEVEL_100_PERCENT',
      '/last-location-bar': 'ThunarLocationEntry',
      '/misc-date-style': 'THUNAR_DATE_STYLE_YYYYMMDD' } ],
  [ 'set', 'keyboards', {
      '/Default/KeyRepeat': True,
      '/Default/KeyRepeat/Delay': 300,
      '/Default/KeyRepeat/Rate': 40} ],
  [ 'set', 'xfwm4', {
      '/general/theme': 'Keramik',
      '/general/prevent_focus_stealing': True,
      '/general/workspace_count': 2,
      '/general/workspace_names': ['Work','Social'] } ],
  [ 'set', 'xfce4-session', {
      '/general/SaveOnExit': False } ],
  [ 'set', 'xfce4-keyboard-shortcuts', {
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
      '"/xfwm4/custom/<Shift><Super>Right"': 'move_window_workspace_2_key' } ],
   [ 'clear', 'xfce4-panel', {
      '/panels': None,
      '/plugins': None } ],
   [ 'set', 'xfce4-panel', {
      # Menu
      '/plugins/plugin-1': 'applicationsmenu',
      '/plugins/plugin-1/button-icon': 'xfce4-panel-menu',
      '/plugins/plugin-1/button-title': 'Menu',
      '/plugins/plugin-1/show-button-title': False,
      '/plugins/plugin-1/show-menu-icons': True,
      '/plugins/plugin-1/show-tooltips': False,
      # Fensterliste
      '/plugins/plugin-2': 'tasklist',
      '/plugins/plugin-2/flat-buttons': True,
      '/plugins/plugin-2/grouping': 1,
      '/plugins/plugin-2/show-handle': True,
      '/plugins/plugin-2/show-wireframes': True,
      '/plugins/plugin-2/window-scrolling': False,
      '/plugins/plugin-2/include-all-workspaces': False,
      # Trenner
      '/plugins/plugin-3': 'separator',
      '/plugins/plugin-3/expand': True,
      '/plugins/plugin-3/style': 0,
      # Arbeitsbereiche
      '/plugins/plugin-4': 'pager',
      '/plugins/plugin-4/miniature-view': True,
      '/plugins/plugin-4/rows': 1,
      '/plugins/plugin-4/workspace-scrolling': False,
      # Trenner
      '/plugins/plugin-5': 'separator',
      '/plugins/plugin-5/expand': False,
      '/plugins/plugin-5/style': 0,
      # Elemente vor Systray
      '/plugins/plugin-6': 'eyes',                  # Augen
      '/plugins/plugin-7': 'screenshooter',         # Bildschirmfoto
      '/plugins/plugin-8': 'weather',               # Wetter
      '/plugins/plugin-9': 'xfce-clipman-plugin',   # Zwischenablage
      '/plugins/plugin-10': 'xkb',                  # Tastatursprache
      '/plugins/plugin-11': 'cpugraph',             # Prozessorauslastung
      '/plugins/plugin-12': 'netload',              # Netzauslastung
      # Systray
      '/plugins/plugin-13': 'systray',              # Externe Elemente
      #'/plugins/plugin-13/names-hidden': [],
      '/plugins/plugin-13/names-ordered': ['pragha musikspieler','Nextcloud','dnfdragora-updater','netzwerk-manager-applet','Keybase','pidgin'],
      '/plugins/plugin-13/show-frame': False,
      '/plugins/plugin-13/size-max': 22,
      '/plugins/plugin-13/square-icons': True,
      # Elemente nach Systray
      '/plugins/plugin-14': 'power-manager-plugin', # Energieverwaltung
      '/plugins/plugin-15': 'notification-plugin',  # Benachrichtigungen
      '/plugins/plugin-16': 'pulseaudio',           # Lautsprecher
      '/plugins/plugin-16/enable-keyboard-shortcuts': True,
      '/plugins/plugin-16/show-notifications': True,
      #'/plugins/plugin-16/mpris-players': 'firefox/instance;pragha',
      '/plugins/plugin-17': 'xfce4-orageclock-plugin', # Datum und Uhrzeit
      '/plugins/plugin-18': 'actions',              # Abmelden etc
      '/plugins/plugin-18/appearance': 1,
      '/plugins/plugin-18/ask-confirmation': True,
      # Starters
      '/plugins/plugin-19': 'launcher',             # Starter 1: Terminal
      '/plugins/plugin-19/items': ['exo-terminal-emulator.desktop'],
      '/plugins/plugin-20': 'launcher',             # Starter 2: Byobu
      '/plugins/plugin-20-/items': ['exo-terminal-byobu.desktop'],
      '/plugins/plugin-21': 'launcher',             # Starter 2: Dateimanager
      '/plugins/plugin-21/items': ['exo-file-manager.desktop'],
      '/plugins/plugin-22': 'launcher',             # Starter 2: Commander
      '/plugins/plugin-22/items': ['exo-file-commander.desktop'],
      '/plugins/plugin-23': 'launcher',             # Starter 4: Firefox
      '/plugins/plugin-23/items': ['exo-firefox.desktop'],
      '/plugins/plugin-24': 'launcher',             # Starter 4: Chrome
      '/plugins/plugin-24/items': ['exo-chromium.desktop'],
      '/plugins/plugin-25': 'separator',
      '/plugins/plugin-25/expand': False,
      '/plugins/plugin-25/style': 1,
      '/plugins/plugin-26': 'directorymenu',        # Schnellzugriff Verzeichnisse
      '/plugins/plugin-26/base-directory': '.',

      # Obere Leiste
      '/panels/panel-1/autohide-behavior': 0,
      '/panels/panel-1/background-style': 1,
      '/panels/panel-1/background-alpha': 100,
      '/panels/panel-1/background-rgba': [0.596078, 0.415686, 0.266667, 1.000000],
      '/panels/panel-1/disable-struts': False,
      '/panels/panel-1/enter-opacity': 100,
      '/panels/panel-1/leave-opacity': 100,
      '/panels/panel-1/length': 100,
      '/panels/panel-1/mode': 0,
      '/panels/panel-1/nrows': 1,
      '/panels/panel-1/plugin-ids': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18],
      '/panels/panel-1/position': 'p=6\;x=0\;y=0',
      '/panels/panel-1/position-locked': True,
      '/panels/panel-1/size': 32,
      # Untere Leiste
      '/panels/panel-2/autohide-behavior': 1,
      '/panels/panel-2/background-style': 1,
      '/panels/panel-2/background-alpha': 100,
      '/panels/panel-2/background-rgba': [0.596078, 0.415686, 0.266667, 1.000000],
      '/panels/panel-2/disable-struts': False,
      '/panels/panel-2/enter-opacity': 100,
      '/panels/panel-2/leave-opacity': 100,
      '/panels/panel-2/length': 10,
      '/panels/panel-2/length-adjust': True,
      '/panels/panel-2/mode': 0,
      '/panels/panel-2/nrows': 1,
      '/panels/panel-2/plugin-ids': [19,20,21,22,23,24,25,26],
      '/panels/panel-2/position': 'p=10\;x=0\;y=0',
      '/panels/panel-2/position-locked': True,
      '/panels/panel-2/size': 48,
      '/panels': [1,2],
    } ]
]

def get_typenames(value):
  if isinstance(value, list):
    result = '-a'
    for key in value:
      result += ' ' + get_typenames(key)
    return result
  if isinstance(value, bool): return '-t bool'
  if isinstance(value, int): return '-t int'
  if isinstance(value, float): return '-t double'
  return '-t string'

def get_values(value):
  if isinstance(value, list):
    result = ''
    for key in value:
      result += get_values(key) + ' '
    return result
  if isinstance(value, str): return '-s ' + value
  if isinstance(value, bool): return '-s ' + str(value).lower()
  return '-s ' + str(value)

def call_xfconf(command, channel, property, value):
  types = get_typenames(value)
  values = get_values(value)

  if command=='set':
    execSet = f'xfconf-query -c {channel} {types} -np {property} {values}'
    print (execSet)
    resultSet = os.popen(execSet).read()
    #execRead = f'xfconf-query -c {channel} -p {property}'
    #resultRead = os.popen(execRead).read()
    # print (resultRead)
  elif command=='clear':
    execClear = f'xfconf-query -c {channel} -p {property} -r -R'
    resultClear = os.popen(execClear).read()
    # print (resultClear)


def configure_settings():
  for step in config_steps:
    command = step[0]
    channel = step[1]
    keys = step[2]
    for key in keys:
      value = keys[key]
      call_xfconf(command, channel, key, value)


def read_plugins():
  readPlugins = 'xfconf-query -c xfce4-panel -p /plugins -l'
  plugins = os.popen(readPlugins).read().splitlines()
  for plugin in plugins:
    index = len('/plugins/plugin-')
    tmp = plugin[index :: ]
    if '/' in tmp: continue

    pluginId = int(tmp)
    namePlugin = f'xfconf-query -c xfce4-panel -p /plugins/plugin-{pluginId}'
    pluginName = os.popen(namePlugin).read().splitlines()[0]

    print (f'Plugin {pluginId} is {pluginName}')


output("<head>=====[ Configuring XFCE ]====<nc>")
configure_settings()
