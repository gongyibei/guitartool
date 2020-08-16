import curses
import random

from chord import CHORD_TYPES, Chord
from color import Fore, Back
from scale import ALL_NOTES
import numpy as np
from player import generate_song, generate_chord, play



class Win:
    def __init__(self, hei, wid, y, x):
        self.win = curses.newwin(hei, wid, y, x)
        self.hei = hei
        self.wid = wid
        self.y = y
        self.x = x

    def build(self):
        pass

    def draw(self):
        self.build()
        self.win.refresh()


class Cantainer(Win):
    def __init__(self, hei, wid, y, x, winlist=[]):
        super().__init__(hei, wid, y, x)
        self.winlist = winlist
        self.nwin = len(self.winlist)

    def draw(self):
        super().draw()
        if self.winlist:
            for win in self.winlist:
                win.draw()


class MenuCard(Win):
    hei = 4
    wid = 20

    def __init__(self, y, x, menu=[None, None], choosed=False):
        super().__init__(self.hei, self.wid, y, x)
        self.choosed = choosed

        title = menu[0]
        if title and len(title) > self.wid - 4:
            title = title[:self.wid - 4]
        self.title = title

        self.items = menu[1]
        self.i = 0
        #  self.cur = self.itmes[self.i]

    def build(self):
        #  if self.choosed:
        #      self.win.box()
        self.win.erase()
        if self.title and self.items:
            self.win.addstr(1, 2 + (self.wid - 4 - len(self.title)) // 2 - 1,
                            self.title)
            if self.choosed:
                self.win.addstr(2, 2, '<<', curses.color_pair(Fore.RED))
                self.win.addstr(2, self.wid - 4, '>>',
                                curses.color_pair(Fore.RED))
            else:
                self.win.addstr(2, 2, '<<')
                self.win.addstr(2, self.wid - 4, '>>')
            self.win.addstr(2,
                            2 + (self.wid - 4 - len(self.items[self.i])) // 2,
                            self.items[self.i])

    def fed(self, menu):
        if menu:
            self.title, self.items = menu

    def getitem(self):
        return self.items[self.i]

    def next(self):
        n = len(self.items)
        self.i = (self.i + 1) % n
        self.cur = self.items[self.i]

    def last(self):
        n = len(self.items)
        self.i = (self.i - 1 + n) % n
        self.cur = self.items[self.i]

    def __str__(self):
        return self.cur.__str__()

    def handle(self, *args):
        if args:
            arg = args[0]
            if self.title and self.items:
                if arg == 'next':
                    self.next()
                elif arg == 'last':
                    self.last()


class PlayerIcon(Win):
    def __init__(self, y, x, interval=0.5):
        self.status = 'stop'
        self.interval = interval
        self.icon = ['🔈', '🔉', '🔊']
        self.i = 0

        super().__init__(1, 1, y, x)

    def addstr():
        if self.status != 'stop':
            self.addstr(self.icon[self.i])

    def start():
        self.status = 'start'
        self.refresh()

    def stop():
        self.status = 'stop'
        self.refresh()


class HelpCard(Win):
    hei = 1
    wid = 35

    def __init__(self, y, x, help=[None, None], choosed=False):
        self.key, self.dsc = help
        super().__init__(10, 35, y, x)

    def build(self):
        if self.key and self.dsc:
            self.win.addstr(0, self.wid // 2 - len(self.key), self.key, curses.color_pair(Fore.RED))
            self.win.addstr(0, self.wid // 2 + 1, self.dsc)

    def fed(self, help):
        if help:
            self.key, self.dsc = help


class ChordCard(Win):
    hei = 10
    wid = 35

    def __init__(self, y, x, chord=[None, None], choosed=False):
        super().__init__(10, 35, y, x)
        self.title, self.chord = chord

        #  self.player = PlayerIcon(y + 1, x - 1)
        self.choosed = choosed
        self.forbid = Fore.RED
        self.pitch_color = Fore.MAGENTA
        self.title_color = Back.BLUE
        self.board_color = Fore.BLUE
        self.left_color = Fore.RED
        self.right_color = Fore.CYAN
        self.bottom_color = Fore.YELLOW
        self.press_position_color = Fore.MAGENTA

        self.symbles = ['🌈', '🐶', '🌀']

    def build(self):
        self.win.erase()

        if self.choosed:
            self.win.attron(curses.color_pair(Fore.RED))
            self.win.box()

        if not self.chord:
            return

        self.win.attron(curses.color_pair(self.board_color))

        chord = [(p[2], p[0], p[1]) for p in self.chord]
        minfret = min(chord, key=lambda p: p[1] if p[1] != 0 else 100)[1]
        maxfret = max(chord, key=lambda p: p[1])[1]
        minfret = min(maxfret - 2, minfret)
        minfret = max(minfret, 1)
        nfret = maxfret - minfret + 1
        nfret = max(nfret, 3)
        startfret = minfret

        symble = self.symbles[1]

        self.win.addstr(2, 2, '×', curses.color_pair(self.left_color))
        self.win.addstr(3, 2, '×', curses.color_pair(self.left_color))
        self.win.addstr(4, 2, '×', curses.color_pair(self.left_color))
        self.win.addstr(5, 2, '×', curses.color_pair(self.left_color))
        self.win.addstr(6, 2, '×', curses.color_pair(self.left_color))
        self.win.addstr(7, 2, '×', curses.color_pair(self.left_color))

        self.win.addstr(1, 4 + (self.wid - 2 - 4 - len(self.title)) // 2 - 1,
                        self.title, curses.color_pair(self.title_color))
        if nfret == 3:
            #  4 - (self.wid - 4 - len(self.title))//2 - 1
            self.win.addstr(2, 3, '┏────────┬────────┬────────┐')
            self.win.addstr(3, 3, '┣────────┼────────┼────────┤')
            self.win.addstr(4, 3, '┣────────┼────────┼────────┤')
            self.win.addstr(5, 3, '┣────────┼────────┼────────┤')
            self.win.addstr(6, 3, '┣────────┼────────┼────────┤')
            self.win.addstr(7, 3, '┗────────┴────────┴────────┘')

            if startfret > 1:
                self.win.addstr(8, 7, str(startfret),
                                curses.color_pair(self.bottom_color))

            for fret, content, string in self.chord:
                if fret == 0:
                    self.win.addstr(1 + string, 2, '○',
                                    curses.color_pair(self.left_color))
                else:
                    self.win.addstr(1 + string, 2, ' ')
                    self.win.addstr(1 + string, 7 + 9 * (fret - startfret),
                                    symble)

                self.win.addstr(1 + string, 31, content,
                                curses.color_pair(self.right_color))

        elif nfret == 4:
            self.win.addstr(2, 3, '┏──────┬──────┬──────┬──────┐')
            self.win.addstr(3, 3, '┣──────┼──────┼──────┼──────┤')
            self.win.addstr(4, 3, '┣──────┼──────┼──────┼──────┤')
            self.win.addstr(5, 3, '┣──────┼──────┼──────┼──────┤')
            self.win.addstr(6, 3, '┣──────┼──────┼──────┼──────┤')
            self.win.addstr(7, 3, '┗──────┴──────┴──────┴──────┘')

            if startfret > 1:
                self.win.addstr(8, 6, str(startfret),
                                curses.color_pair(self.bottom_color))

            for fret, content, string in self.chord:
                if fret == 0:
                    self.win.addstr(1 + string, 2, '○',
                                    curses.color_pair(self.left_color))
                else:
                    self.win.addstr(1 + string, 2, ' ')
                    self.win.addstr(1 + string, 6 + 7 * (fret - startfret),
                                    symble)

                self.win.addstr(1 + string, 32, content,
                                curses.color_pair(self.right_color))

    def fed(self, chord):
        if chord:
            self.title, self.chord = chord

    def handle(self, *args):
        if self.chord:
            start = [16, 11, 7, 2, -3, -8]
            song = []
            chord = []
            for fret, _, string in self.chord:
                semi = start[string - 1] + fret - 12
                song.append([semi, 1])
                chord.append(semi)
            song[-1][-1] = 2

            audio = generate_song(song, 0.1)
            #  chord = generate_chord(chord, 2)
            play(audio)
            #  play(chord)

    def getitem(self):
        return self.title


class Matrix(Cantainer):
    def __init__(self, hei, wid, y, x, Card, nrow=100, ncol=100, items=[]):

        self.nrow = min(hei // Card.hei, nrow)
        self.ncol = min(wid // Card.wid, ncol)
        y = y + (hei - Card.hei * self.nrow) // 2
        x = x + (wid - Card.wid * self.ncol) // 2
        hei = Card.hei * self.nrow
        wid = Card.wid * self.ncol
        winlist = []
        for r in range(self.nrow):
            for c in range(self.ncol):
                winlist.append(Card(y + r * Card.hei, x + c * Card.wid))
        super().__init__(hei, wid, y, x, winlist=winlist)
        self.items = items
        self.nitems = len(self.items)
        self.first = 0
        self.row = 0
        self.col = 0
        self.winlist[self.first].choosed = True
        self.fedall()

    def fedall(self):
        for r in range(self.nrow):
            for c in range(self.ncol):
                i = r * self.ncol + c

                if i + self.first < len(self.items):
                    self.winlist[i].fed(self.items[i + self.first])
                else:
                    self.winlist[i].fed(None)

    def move(self, drow, dcol):
        i = self.row * self.ncol + self.col
        self.winlist[i].choosed = False
        self.row += drow
        self.col += dcol
        i = self.row * self.ncol + self.col
        self.winlist[i].choosed = True

    def up(self):
        if self.row > 0:
            self.move(-1, 0)
        elif self.first != 0:
            self.first -= self.ncol
            self.fedall()

    def down(self):
        if self.row < self.nrow - 1 and self.first + (
                self.row + 1) * self.ncol - 1 < len(self.items) - 1:
            self.move(1, 0)
        elif self.first + self.nrow * self.ncol - 1 < len(self.items) - 1:
            self.first += self.ncol
            self.fedall()

    def left(self):
        if self.col > 0:
            self.move(0, -1)

    def right(self):
        if self.col < self.ncol - 1:
            self.move(0, 1)

    def handle(self, *args):
        i = self.row * self.ncol + self.col
        self.winlist[i].handle(*args)

    def getitems(self):
        items = []
        for win in self.winlist[:2]:
            items.append(win.getitem())
        return items

    def refresh(self):
        i = self.row * self.ncol + self.col
        self.winlist[i].choosed = False

        self.nitems = len(self.items)
        self.first = 0
        self.row = 0
        self.col = 0
        self.winlist[self.first].choosed = True
        self.fedall()


class Box(Cantainer):
    def __init__(self,
                 hei,
                 wid,
                 y,
                 x,
                 matrix,
                 winlist=[],
                 choosed=False,
                 title='Untitled'):
        super().__init__(hei, wid, y, x, winlist=winlist)
        self.matrix = matrix
        self.choosed = choosed
        if len(title) > self.wid - 4:
            title = title[:self.wid - 4]
        self.title = title

        self.color = Fore.WHITE

    def build(self):
        if self.choosed:
            self.boxcolor = Fore.CYAN
        else:
            self.boxcolor = Fore.WHITE
        # draw box
        self.win.attron(curses.color_pair(self.boxcolor))
        self.win.box()

        # draw title
        self.win.addstr(0, 2 + (self.wid - 4 - len(self.title)) // 2 - 1,
                        self.title)


class Ui(Cantainer):
    def __init__(self):
        curses.initscr()
        curses.noecho()
        super().__init__(curses.LINES, curses.COLS, 0, 0)
        self.ration = (1, 4)

        self.init_color()
        self.footer = self.init_footer()
        self.left = self.init_left()
        self.right = self.init_right()
        self.curbox = self.left

    def init_footer(self):
        help = [
            ['K','上'],
            ['J','下'],
            ['H','左'],
            ['L','右'],
            ['TAB','切换窗口'],
            ['SPACE','播放'],
            ['R','刷新'],
            ['Q','退出'],
        ]
        footer = Matrix(2, self.wid, self.hei - 3, 0, HelpCard, items=help)
        self.winlist.append(footer)
        return footer

    def init_left(self):
        hei, wid, y, x = self.hei - 3, self.wid // sum(
            self.ration) * self.ration[0], 0, 0
        menus = [
            ['根  音', ALL_NOTES],
            ['类  型', list(CHORD_TYPES.keys())],
        ]
        matrix = Matrix(hei - 2, wid - 2, y + 1, x + 1, MenuCard, ncol=1, items=menus)
        left = Box(hei, wid, y, x, matrix, winlist=[matrix], choosed=True, title='设置')
        self.winlist.append(left)
        return left

    def init_right(self):
        chords = self.get_chords(ALL_NOTES[0], list(CHORD_TYPES.keys())[0])
        hei, wid, y, x = self.hei - 3, self.wid // sum(
            self.ration) * self.ration[1], 0, self.wid // sum(
                self.ration) * self.ration[0]
        matrix = Matrix(hei - 2, wid - 2, y + 1, x + 1, ChordCard, items=chords)
        right = Box(hei, wid, y, x, matrix, winlist=[matrix], title='和弦')
        self.winlist.append(right)
        return right



    def init_color(self):
        curses.start_color()
        curses.use_default_colors()
        # Fore
        curses.init_pair(Fore.BLACK, curses.COLOR_BLACK, -1)
        curses.init_pair(Fore.RED, curses.COLOR_RED, -1)
        curses.init_pair(Fore.GREEN, curses.COLOR_GREEN, -1)
        curses.init_pair(Fore.YELLOW, curses.COLOR_YELLOW, -1)
        curses.init_pair(Fore.BLUE, curses.COLOR_BLUE, -1)
        curses.init_pair(Fore.MAGENTA, curses.COLOR_MAGENTA, -1)
        curses.init_pair(Fore.CYAN, curses.COLOR_CYAN, -1)
        curses.init_pair(Fore.WHITE, curses.COLOR_WHITE, -1)

        # Back
        curses.init_pair(Back.BLACK, -1, curses.COLOR_BLACK)
        curses.init_pair(Back.RED, -1, curses.COLOR_RED)
        curses.init_pair(Back.GREEN, -1, curses.COLOR_GREEN)
        curses.init_pair(Back.YELLOW, -1, curses.COLOR_YELLOW)
        curses.init_pair(Back.BLUE, -1, curses.COLOR_BLUE)
        curses.init_pair(Back.MAGENTA, -1, curses.COLOR_MAGENTA)
        curses.init_pair(Back.CYAN, -1, curses.COLOR_CYAN)
        curses.init_pair(Back.WHITE, -1, curses.COLOR_WHITE)
        curses.curs_set(0)

    def change_box(self):
        if self.curbox == self.left:
            self.curbox = self.right
            self.left.choosed = False
            self.right.choosed = True
        else:
            self.curbox = self.left
            self.left.choosed = True
            self.right.choosed = False

    def get_chords(self, *args):
        base = args[0]
        type = args[1]
        filters = {
            'OpenChords': 0,
            'Barrechord': 0,
            'inversion': 1,
            'strings': [
                [6, 5, 4, 3, 2, 1],
                [5, 4, 3, 2, 1],
                [4, 3, 2, 1],
                [6, 4, 3, 2],
                [5, 4, 3, 2],
            ],
            'gap': 4,
            'ignor': []
        }
        chords = Chord(base=base, type=type).get_positions(filters=filters)
        chords.sort(
            key=lambda c: min(c, key=lambda p: p[0] if p[0] != 0 else 100)[0])
        chords = [[f' {base}{type} ', chord] for chord in chords]
        return chords

    def exit(self):
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def loop(self):
        self.draw()
        k = self.win.getch()
        while True:
            if k == ord('q'):
                self.exit()
                break
            elif k == ord('\t'):
                self.change_box()
            if k == ord('k'):
                self.curbox.matrix.up()
            elif k == ord('j'):
                self.curbox.matrix.down()
            elif k == ord('h'):
                if self.curbox == self.left:
                    self.curbox.matrix.handle('last')
                elif self.curbox == self.right:
                    self.curbox.matrix.left()
            elif k == ord('l'):
                if self.curbox == self.left:
                    self.curbox.matrix.handle('next')
                elif self.curbox == self.right:
                    self.curbox.matrix.right()
            elif k == ord(' '):
                self.curbox.matrix.handle()
            elif k == ord('r'):
                items = self.left.matrix.getitems()
                self.right.matrix.items = self.get_chords(*items)
                self.right.matrix.refresh()

            self.draw()
            k = self.win.getch()


if __name__ == '__main__':
    Ui().loop()
