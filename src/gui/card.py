import curses
import threading

from .win import Win
from src.util.color import Fore, Back
from src.util.player import generate_song_by_fluidsynth, play
from ..util.log import LOG
from ..util.setting import NOTE_SYMBOLS, NUMBER_SYMBOLS


class Card(Win):
    def __init__(self, hei, wid, y, x, item=None, choosed=False):
        super().__init__(hei, wid, y, x)
        self.item = item
        self.choosed = choosed

    def choose(self):
        self.choosed = True

    def unchoose(self):
        self.choosed = False

    def fed(self, item):
        self.item = item

    def get(self):
        return self.item

    def handel(self):
        pass


class MenuCard(Card):
    hei = 4
    wid = 20

    def __init__(self, y, x, item=None, choosed=False):
        super().__init__(self.hei, self.wid, y, x, item=item, choosed=choosed)

    def strwid(self, str):
        wid = 0
        for ch in str:
            if ch.isascii():
                wid += 1
            else:
                wid += 2
        return wid

    def build(self):
        if self.item:
            title = self.item.title
            cur = self.item.cur
            if title and len(title) > self.wid - 4:
                title = title[:self.wid - 4]

            self.addstr(1, 2 + (self.wid - 4 - self.strwid(title)) // 2,
                        title)
            if self.choosed:
                self.addstr(2, 2, '<<', curses.color_pair(Fore.RED))
                self.addstr(2, self.wid - 4, '>>', curses.color_pair(Fore.RED))
            else:
                self.addstr(2, 2, '<<')
                self.addstr(2, self.wid - 4, '>>')
            self.addstr(2, 2 + (self.wid - 4 - self.strwid(cur)) // 2, cur)


class HelpCard(Card):
    hei = 1
    wid = 35

    def __init__(self, y, x, item=None):
        super().__init__(self.hei, self.wid, y, x, item=item)

    def build(self):
        if self.item:
            key, dsc = self.item
            self.addstr(0, self.wid // 2 - len(key), key, curses.color_pair(Fore.RED))
            self.addstr(0, self.wid // 2 + 1, dsc)


class ChordCard(Card):
    hei = 10
    wid = 35

    def __init__(self, y, x, item=None, choosed=False):
        super().__init__(self.hei, self.wid, y, x, item=item, choosed=choosed)
        #  self.player = PlayerIcon(y + 1, x - 1)
        self.forbid = Fore.RED
        self.pitch_color = Fore.MAGENTA
        self.title_color = Back.BLUE
        self.board_color = Fore.BLUE
        self.left_color = Fore.RED
        self.right_color = Fore.CYAN
        self.bottom_color = Fore.YELLOW
        self.press_position_color = Fore.MAGENTA

    def build(self):
        if self.choosed:
            self.attron(curses.color_pair(Fore.RED))
            self.box()

        if self.item:
            title = self.item.title
            chord = self.item.chord
        else:
            return

        self.attron(curses.color_pair(self.board_color))

        chord_ = [(p[2], p[0], p[1]) for p in chord]
        minfret = min(chord_, key=lambda p: p[1] if p[1] != 0 else 100)[1]
        maxfret = max(chord_, key=lambda p: p[1])[1]
        minfret = min(maxfret - 2, minfret)
        startfret = max(minfret, 1)
        nfret = max(maxfret - minfret + 1, 3)

        symble = self.item.symble

        left_x, left_y = 2, 2
        for i in range(6):
            self.addstr(i + left_y, left_x, '×', curses.color_pair(self.left_color))

        self.addstr(1, 4 + (self.wid - 2 - 4 - len(title)) // 2 - 1,
                    title, curses.color_pair(self.title_color))
        fret_start = 3
        if nfret == 3:
            self.addstr(2, fret_start, '┏────────┬────────┬────────┐')
            self.addstr(3, fret_start, '┣────────┼────────┼────────┤')
            self.addstr(4, fret_start, '┣────────┼────────┼────────┤')
            self.addstr(5, fret_start, '┣────────┼────────┼────────┤')
            self.addstr(6, fret_start, '┣────────┼────────┼────────┤')
            self.addstr(7, fret_start, '┗────────┴────────┴────────┘')

            fret_wid = 9
            offset = 7
            right_x = 31

        elif nfret == 4:
            self.addstr(2, fret_start, '┏──────┬──────┬──────┬──────┐')
            self.addstr(3, fret_start, '┣──────┼──────┼──────┼──────┤')
            self.addstr(4, fret_start, '┣──────┼──────┼──────┼──────┤')
            self.addstr(5, fret_start, '┣──────┼──────┼──────┼──────┤')
            self.addstr(6, fret_start, '┣──────┼──────┼──────┼──────┤')
            self.addstr(7, fret_start, '┗──────┴──────┴──────┴──────┘')

            fret_wid = 7
            offset = 6
            right_x = 32

        if startfret > 1:
            self.addstr(8, offset, str(startfret),
                        curses.color_pair(self.bottom_color))

        for fret, content, string in chord:
            if fret == 0:
                self.addstr(1 + string, 2, '○',
                            curses.color_pair(self.left_color))
            else:
                self.addstr(1 + string, 2, ' ')
                self.addstr(1 + string, offset + fret_wid * (fret - startfret), symble)

            self.addstr(1 + string, right_x, content,
                        curses.color_pair(self.right_color))

    def play(self):
        if self.item:
            start = [16, 11, 7, 2, -3, -8]
            song = []
            chord = []
            for fret, _, string in self.item.chord:
                semi = start[string - 1] + fret - 12
                song.append([semi, 1])
                chord.append(semi)
            song[-1][-1] = 2

            #  audio = generate_song(song, 0.3)
            data = generate_song_by_fluidsynth(song, 0.15, instrument=self.item.instrument)
            #  chord = generate_chord(chord, 2)
            threading.Thread(target=play, args=(data,), daemon=True).start()


class BoardCard(Card):
    hei = 10
    wid = 88

    def __init__(self, y, x, item=None, choosed=False):
        super().__init__(self.hei, self.wid, y, x, item=item, choosed=choosed)
        self.forbid = Fore.RED
        self.pitch_color = Fore.MAGENTA
        self.title_color = Back.BLUE
        self.board_color = Fore.BLUE
        self.root_color = Fore.RED
        self.note_color = Fore.BLUE
        self.bottom_color = Fore.YELLOW
        self.press_position_color = Fore.MAGENTA

    def build(self):
        self.attron(curses.color_pair(self.board_color))

        root = self.item.root
        title = self.item.title
        strings = self.item.strings
        openstring = self.item.openstring

        self.addstr(1, 4 + (self.wid - 2 - 4 - len(title)) // 2 - 1,
                    title, curses.color_pair(self.title_color))



        fret_start = 2
        self.addstr(2, fret_start, '┏───' + '───┬───' * 11 + '───┐')
        self.addstr(3, fret_start, '┣───' + '───┼───' * 11 + '───┤')
        self.addstr(4, fret_start, '┣───' + '───┼───' * 11 + '───┤')
        self.addstr(5, fret_start, '┣───' + '───┼───' * 11 + '───┤')
        self.addstr(6, fret_start, '┣───' + '───┼───' * 11 + '───┤')
        self.addstr(7, fret_start, '┗───' + '───┴───' * 11 + '───┘')

        self.addstr(8, fret_start + 3, '1', curses.color_pair(self.bottom_color))
        self.addstr(8, fret_start + 3 + 14, '3', curses.color_pair(self.bottom_color))
        self.addstr(8, fret_start + 3 + 14*2, '5', curses.color_pair(self.bottom_color))
        self.addstr(8, fret_start + 3 + 14*3, '7', curses.color_pair(self.bottom_color))
        self.addstr(8, fret_start + 3 + 14*4, '9', curses.color_pair(self.bottom_color))
        self.addstr(8, fret_start + 3 + 14*5 + 7, '12', curses.color_pair(self.bottom_color))

        for i, symbol in enumerate(openstring):
            if symbol:
                if symbol == NUMBER_SYMBOLS['1'] or symbol == NOTE_SYMBOLS[root]:
                    color = self.root_color
                else:
                    color = self.note_color
                self.addstr(2 + i, 0, symbol, curses.color_pair(color))
        for i, string in enumerate(strings):
            for j, symbol in enumerate(string):
                if symbol:
                    if symbol == NUMBER_SYMBOLS['1'] or symbol == NOTE_SYMBOLS[root]:
                        color = self.root_color
                    else:
                        color = self.note_color
                    if len(symbol) == 1:
                        self.addstr(i + 2, fret_start + 3 + j*7, symbol + ' ', curses.color_pair(color))
                    else:
                        self.addstr(i + 2, fret_start + 3 + j*7 - 1, symbol + ' ', curses.color_pair(color))






