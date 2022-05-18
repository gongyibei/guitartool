import curses
import math

from .card import *
from .container import Container, Matrix
from ..util.color import Fore


class Page(Container):
    def __init__(self,
                 hei,
                 wid,
                 y,
                 x,
                 chosen=False,
                 title='Untitled'):
        super().__init__(hei, wid, y, x)
        self.chosen = chosen
        if len(title) > self.wid - 4:
            title = title[:self.wid - 4]
        self.title = title
        self.color = Fore.WHITE

    def build(self):
        if self.chosen:
            self.color = Fore.CYAN
        else:
            self.color = Fore.WHITE

        # draw box
        self.attron(curses.color_pair(self.color))
        self.box()

        # draw title
        self.addstr(0, 2 + (self.wid - 4 - len(self.title)) // 2 - 1,
                    self.title)

    def choose(self):
        self.chosen = True

    def unchoose(self):
        self.chosen = False


class MatrixPage(Page):
    def __init__(self, hei, wid, y, x, Card, items=None, chosen=True, title='Untitled', nrow=100,
                 ncol=100):
        self.matrix = Matrix(hei - 2,
                             wid - 2,
                             y + 1,
                             x + 1,
                             Card,
                             nrow=nrow,
                             ncol=ncol)
        super().__init__(hei, wid, y, x, chosen=chosen, title=title)
        self.items = items
        self.n = len(self.items)
        self.matrix = Matrix(hei - 2,
                             wid - 2,
                             y + 1,
                             x + 1,
                             Card,
                             nrow=nrow,
                             ncol=ncol)
        self.add(self.matrix)
        LOG.info(title)
        LOG.info(self.winlist)
        self.nrow = self.matrix.nrow
        self.ncol = self.matrix.ncol
        self.ncard = self.nrow * self.ncol

        self.col = 0
        self.row = 0
        self.first = 0
        self.matrix[0, 0].choose()
        self.fedcur()


    @property
    def curi(self):
        return self.first + self.row * self.ncol

    @property
    def curcard(self):
        return self.matrix[self.row, self.col]

    def fedcur(self):
        self.matrix.fedall(self.items[self.first:self.first + self.ncard])

    def _move(self, drow, dcol):
        self.curcard.unchoose()
        self.row += drow
        self.col += dcol
        self.curcard.choose()

    def up(self):
        if self.row > 0:
            self._move(-1, 0)
        elif self.first != 0:
            self.first -= self.ncol
            self.fedcur()

    def down(self):
        if math.ceil((self.curi + 1 + self.ncol) / self.ncol) <= math.ceil(self.n / self.ncol):
            if self.row + 1 < self.nrow:
                self._move(1, 0)
            else:
                self.first += self.ncol
                self.fedcur()

    def left(self):
        if self.col > 0:
            self._move(0, -1)

    def right(self):
        if self.col < self.ncol - 1:
            self._move(0, 1)

    def update(self, items):
        self.matrix[self.row, self.col].unchoose()
        self.items = items
        self.n = len(self.items)
        self.col = 0
        self.row = 0
        self.first = 0
        self.matrix[0, 0].choose()
        self.fedcur()


class MenuPage(MatrixPage):
    def __init__(self, hei, wid, y, x, items=None, chosen=True):
        super().__init__(hei, wid, y, x, MenuCard, items=items, chosen=chosen, title='设置')

    def next(self):
        self.items[self.curi].next()

    def last(self):
        self.items[self.curi].last()

    def handle(self, k):
        if k == 'k':
            self.up()
        elif k == 'j':
            self.down()
        elif k == 'l':
            self.next()
        elif k == 'h':
            self.last()

    def get_menu(self):
        items = []
        for item in self.items:
            items.append(item.cur)
        return items


class ChordPage(MatrixPage):
    def __init__(self, hei, wid, y, x, items=None, chosen=False):
        super().__init__(hei, wid, y, x, ChordCard, items=items, chosen=chosen, title='和弦')

    def handle(self, k):
        if k == 'k':
            self.up()
        elif k == 'j':
            self.down()
        elif k == 'h':
            self.left()
        elif k == 'l':
            self.right()
        elif k == ' ':
            self.curcard.play()

class BoardPage(MatrixPage):
    def __init__(self, hei, wid, y, x, items=None, chosen=False):
        super().__init__(hei, wid, y, x, BoardCard, items=items, chosen=chosen, title='音阶', nrow=1, ncol=1)

    def handle(self, k):
        pass
