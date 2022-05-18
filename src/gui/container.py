import curses
import math

from .win import Win
from src.util.color import Fore
from ..util.log import LOG


class Container(Win):
    def __init__(self, hei, wid, y, x):
        super().__init__(hei, wid, y, x)
        self.winlist = []

    def draw(self):
        super().draw()
        LOG.info(f'{len(self.winlist)}, {self.winlist}')
        for i, win in enumerate(self.winlist):
            win.draw()

    def add(self, win):
        self.winlist.append(win)


class Matrix(Container):
    def __init__(self, hei, wid, y, x, Card, nrow=100, ncol=100):
        self.nrow = min(hei // Card.hei, nrow)
        self.ncol = min(wid // Card.wid, ncol)
        y = y + (hei - Card.hei * self.nrow) // 2
        x = x + (wid - Card.wid * self.ncol) // 2
        hei = Card.hei * self.nrow
        wid = Card.wid * self.ncol
        super().__init__(hei, wid, y, x)
        for r in range(self.nrow):
            for c in range(self.ncol):
                self.add(Card(y + r * Card.hei, x + c * Card.wid))

        # super().__init__(hei, wid, y, x)
        # self.nrow = min(hei // Card.hei, nrow)
        # self.ncol = min(wid // Card.wid, ncol)
        # y = y + (hei - Card.hei * self.nrow) // 2
        # x = x + (wid - Card.wid * self.ncol) // 2
        # for r in range(self.nrow):
        #     for c in range(self.ncol):
        #         self.winlist.append(Card(y + r * Card.hei, x + c * Card.wid))
        # self.fedall(items)

    def __getitem__(self, indices):
        row, col = indices
        return self.winlist[row*self.ncol + col]

    def fedall(self, items):
        if items:
            for r in range(self.nrow):
                for c in range(self.ncol):
                    i = r * self.ncol + c
                    if i < len(items):
                        self.winlist[i].fed(items[i])
                    else:
                        self.winlist[i].fed(None)




