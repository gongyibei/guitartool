import curses

curses.initscr()
curses.noecho()
curses.curs_set(0)


class Win:
    origin_win = curses.newwin(curses.LINES, curses.COLS, 0, 0)

    def __init__(self, hei, wid, y, x):
        self.win = self.origin_win.subwin(hei, wid, y, x)
        self.hei = hei
        self.wid = wid
        self.y = y
        self.x = x

    def build(self):
        pass

    def refresh(self, *args, **kwargs):
        self.win.refresh(*args, **kwargs)

    def draw(self):
        self.erase()
        self.build()
        self.refresh()

    def addstr(self, *args, **kwargs):
        return self.win.addstr(*args, **kwargs)

    def attron(self, *args, **kwargs):
        return self.win.attron(*args, **kwargs)

    def getch(self, *args, **kwargs):
        return self.win.getch(*args, **kwargs)

    def getkey(self, *args, **kwargs):
        return self.win.getkey(*args, **kwargs)

    def erase(self, *args, **kwargs):
        return self.win.erase(*args, **kwargs)

    def box(self, *args, **kwargs):
        return self.win.box(*args, **kwargs)
