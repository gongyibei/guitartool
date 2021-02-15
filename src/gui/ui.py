import time

from src.gui.item import MenuItem, ChordItem, BoardItem
from src.gui.page import MenuPage, ChordPage, BoardPage
from src.guitar.board import Board
from src.guitar.chord import CHORD_TYPES, Chord
from src.guitar.scale import ALL_NOTES, get_all_scale, all_scale
from src.guitar.tuning import TUNINGS
from src.util.log import LOG
from src.util.player import INSTRUMENTS
import random

from src.util.setting import CHORD_SYMBOLS, NUMBER_SYMBOLS
from .container import *
from .card import *



class Ui(Win):
    def __init__(self):
        curses.initscr()
        curses.noecho()
        super().__init__(curses.LINES, curses.COLS, 0, 0)
        self.ration = (1, 4)
        self._init_color()
        self.footer = self._init_footer()
        self.chord_tab = self._init_chord_tab()
        self.board_tab = self._init_board_tab()
        self.cur_tab = self.chord_tab



    def _init_footer(self):
        help = [
            ['K', '上'],
            ['J', '下'],
            ['H', '左'],
            ['L', '右'],
            ['TAB', '切换窗口'],
            ['SPACE', '播放'],
            ['R', '刷新'],
            ['Q', '退出'],
        ]
        footer = Matrix(2, self.wid, self.hei - 3, 0, HelpCard)
        footer.fedall(help)
        # self.winlist.append(footer)
        return footer

    def _init_chord_tab(self):
        menus = [
            MenuItem('根  音', ALL_NOTES),
            MenuItem('类  型', list(CHORD_TYPES.keys())),
            MenuItem('开  闭', ['全部', '开放和弦', '封闭和弦']),
            MenuItem('转  位', ['原位', '全部']),
            MenuItem('调  弦', list(TUNINGS.keys())),
            MenuItem('音  色', list(INSTRUMENTS.keys())),
            MenuItem('符  号', ['随机'] + CHORD_SYMBOLS),
        ]
        menu = MenuPage(self.hei - 3,
                        self.wid // sum( self.ration) * self.ration[0],
                        0,
                        0,
                        items=menus,
                        chosen=True)
        LOG.info(f'the menu of chord tab created. winlist:{menu.winlist}')

        chords = self.get_chord(*[item.cur for item in menus])
        page = ChordPage(self.hei - 3,
                         self.wid // sum(self.ration) * self.ration[1],
                         0,
                         self.wid // sum(self.ration) * self.ration[0],
                         items=chords,
                         chosen=False)
        LOG.info(f'the page of chord tab created. winlist:{page.winlist}')
        return {'name': 'chord', 'menu': menu, 'page': page, 'cur_page': 'menu'}

    def _init_board_tab(self):
        menus = [
            MenuItem('主  音', ALL_NOTES),
            MenuItem('类  型', list(all_scale.keys())),
            MenuItem('调  弦', list(TUNINGS.keys())),
            MenuItem('符  号', ['音名', '数字']),
        ]
        menu = MenuPage(self.hei - 3,
                        self.wid // sum( self.ration) * self.ration[0],
                        0,
                        0,
                        items=menus,
                        chosen=True)

        LOG.info(f'the menu of chord tab created. winlist:{menu.winlist}')

        boards = self.get_board(*[item.cur for item in menus])
        page = BoardPage(self.hei - 3,
                         self.wid // sum(self.ration) * self.ration[1],
                         0,
                         self.wid // sum(self.ration) * self.ration[0],
                         items=boards,
                         chosen=False)

        LOG.info(f'the page of chord tab created. winlist:{page.winlist}')
        return {'name': 'board', 'menu': menu, 'page': page, 'cur_page': 'menu'}


    def _init_color(self):
        curses.start_color()
        curses.use_default_colors()

        # Initial foreground colors
        curses.init_pair(Fore.BLACK, curses.COLOR_BLACK, -1)
        curses.init_pair(Fore.RED, curses.COLOR_RED, -1)
        curses.init_pair(Fore.GREEN, curses.COLOR_GREEN, -1)
        curses.init_pair(Fore.YELLOW, curses.COLOR_YELLOW, -1)
        curses.init_pair(Fore.BLUE, curses.COLOR_BLUE, -1)
        curses.init_pair(Fore.MAGENTA, curses.COLOR_MAGENTA, -1)
        curses.init_pair(Fore.CYAN, curses.COLOR_CYAN, -1)
        curses.init_pair(Fore.WHITE, curses.COLOR_WHITE, -1)

        # Initial background colors
        curses.init_pair(Back.BLACK, -1, curses.COLOR_BLACK)
        curses.init_pair(Back.RED, -1, curses.COLOR_RED)
        curses.init_pair(Back.GREEN, -1, curses.COLOR_GREEN)
        curses.init_pair(Back.YELLOW, -1, curses.COLOR_YELLOW)
        curses.init_pair(Back.BLUE, -1, curses.COLOR_BLUE)
        curses.init_pair(Back.MAGENTA, -1, curses.COLOR_MAGENTA)
        curses.init_pair(Back.CYAN, -1, curses.COLOR_CYAN)
        curses.init_pair(Back.WHITE, -1, curses.COLOR_WHITE)
        curses.curs_set(0)

    def change_tab(self):
        if self.cur_tab == self.chord_tab:
            self.cur_tab = self.board_tab
        else:
            self.cur_tab = self.chord_tab

    def change_page(self):
        if self.cur_tab['cur_page'] == 'menu':
            self.cur_tab['cur_page'] = 'page'
            self.cur_tab['menu'].unchoose()
            self.cur_tab['page'].choose()
        else:
            self.cur_tab['cur_page'] = 'menu'
            self.cur_tab['menu'].choose()
            self.cur_tab['page'].unchoose()

    def get_board(self, *args):
        root = args[0]
        scale = all_scale[args[1]]
        tuning = args[2]
        symbol_type = args[3]
        tuning = TUNINGS[tuning]
        symbols = []
        board = Board(tuning)
        open_string = []
        if symbol_type == '音名':
            note2symbols = NOTE_SYMBOLS
            strings = board.strings
            notes = scale.notes(root)
        else:
            note2symbols = NUMBER_SYMBOLS
            strings = board.get_pitchs(root)
            notes = scale.pitchs

        for string in strings[::-1]:
            tmp = []
            for note in string:
                if note in notes:
                    tmp.append(note2symbols[note])
                else:
                    tmp.append(None)
            symbols.append(tmp[1:] + tmp[:1])
            open_string.append(tmp[0])

        title = f' {root} {scale.zh_name} '
        return [BoardItem(root, title, symbols, open_string)]


    def get_chord(self, *args):
        base = args[0]
        type = args[1]
        if args[2] == '全部':
            openchords = 0
            barrechord = 0
        elif args[2] == '开放和弦':
            openchords = 0
            barrechord = 1
        elif args[2] == '封闭和弦':
            openchords = 1
            barrechord = 0

        if args[3] == '原位':
            inversion = 1
        elif args[3] == '全部':
            inversion = 0
        else:
            inversion = 0

        tuning = args[4]
        instrument = args[5]

        filters = {
            'openchords':
            openchords,
            'barrechord':
            barrechord,
            'inversion':
            inversion,
            'strings': [
                [6, 5, 4, 3, 2, 1],
                [5, 4, 3, 2, 1],
                [4, 3, 2, 1],
                [6, 4, 3, 2],
                [5, 4, 3, 2],
            ],
            'gap':
            4,
            'ignore': []
        }
        chords = Chord(base, type, tuning).get_positions(filters=filters)
        chords.sort(
            key=lambda c: min(c, key=lambda p: p[0] if p[0] != 0 else 100)[0])

        if args[6] == '随机':
            chords = [ChordItem(f' {base}{type} ', chord, instrument, random.choice(['🐮', '🌈', '🐶', '🌀'])) for chord in chords]
        else:
            chords = [ChordItem(f' {base}{type} ', chord, instrument, args[6]) for chord in chords]

        return chords

    def get_items(self, menu):
        if self.cur_tab == self.chord_tab:
            items = self.get_chord(*menu)
        elif self.cur_tab == self.board_tab:
            items = self.get_board(*menu)
        return items

    def exit(self):
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def draw(self):
        LOG.info(f'Start draw UI, current tab:{self.cur_tab["name"]}')

        LOG.info('start draw menu')
        self.cur_tab['menu'].draw()
        LOG.info('the menu is drawn')

        LOG.info('start draw page')
        self.cur_tab['page'].draw()
        LOG.info('the page is drawn')

        self.footer.draw()

    def loop(self):
        self.draw()
        while True:
            k = self.getch()
            k = chr(k)
            if k == 'q':
                LOG.info('quit')
                self.exit()
                break
            elif k == '`':
                LOG.info('change tab')
                self.change_tab()
                self.draw()
            elif k == '\t':
                LOG.info('change page')
                self.change_page()
                self.draw()
            elif k == 'r':
                LOG.info('refresh')
                menu = self.cur_tab['menu'].get_menu()
                items = self.get_items(menu)
                self.cur_tab['page'].update(items)
                self.draw()
            elif k in set('hjkl '):
                LOG.info('handle')
                cur_page = self.cur_tab['cur_page']
                cur_page = self.cur_tab[cur_page]
                cur_page.handle(k)
                cur_page.draw()


if __name__ == '__main__':
    Ui().loop()
