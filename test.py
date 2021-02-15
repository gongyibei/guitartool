import curses

def loop():
    curses.initscr()
    curses.noecho()
    win1 = curses.newwin(curses.LINES, curses.COLS, 0, 0)
    win1.addstr(10, 10, 'hello')
    win1.refresh()
    win2 = curses.newwin(curses.LINES, curses.COLS, 0, 0)
    while True:
        win2.getch()


loop()
