import curses


def startup():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    return stdscr


def shutdown(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


def main(w):
    win = curses.newwin(1, 1, curses.LINES-1, curses.COLS-1)
    pad = curses.newpad(100, 100)
    pad.addstr('Hello world')
    win.refresh()
    w.getch()


if __name__ == '__main__':
    curses.wrapper(main)