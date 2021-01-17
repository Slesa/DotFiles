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
      '/Default/KeyRepeat/Delay': 300,
      '/Default/KeyRepeat/Rate': 40} ],
  [ 'set', 'xfwm4', {
      '/general/theme': 'Keramik',
      '/general/prevent_focus_stealing': True,
      '/general/workspace_count': 2,
      '/general/workspace_names': '["Work", "Social"]' } ],
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
      '"/xfwm4/custom/<Shift><Super>Right"': 'move_window_workspace_2_key',
   }]
]

def get_typename(value):
  if value is int: return 'int'
  if value is bool: return 'bool'
  return 'string'

def get_value(value):
  if value is str: return value
  if value is bool: return str(value).lower()
  return str(value)

def call_xfconf(command, channel, property, value):
  type = get_typename(value)
  value = get_value(value)
  execSet = f'xfconf-query -c {channel} -t {type} -np {property} -s {value}'
  print (execSet)
  resultSet = os.popen(execSet).read()

  execRead = f'xfconf-query -c {channel} -p {property}'
  resultRead = os.popen(execRead).read()
  # print (resultRead)

def configure_settings():
  for step in config_steps:
    command = step[0]
    channel = step[1]
    keys = step[2]
    for key in keys:
      value = keys[key]
      call_xfconf(command, channel, key, value)


output("<head>=====[ Configuring XFCE ]====<nc>")
#configure_settings()
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
