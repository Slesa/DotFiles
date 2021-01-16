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

configuration = {
    'thunar': {
        'default-view': 'ThunarDetailsView',
        'last-icon-view-zoom-level': 'THUNAR_ZOOM_LEVEL_100_PERCENT',
        'last-location-bar': 'ThunarLocationEntry',
        'misc-date-style': 'THUNAR_DATE_STYLE_YYYYMMDD'
        },
    'keyboards': {
        'Default/KeyRepeat/Delay': 300,
        'Default/KeyRepeat/Rate': 40
        }
}

output("<head>=====[ Configuring XFCE ]====<nc>")
