
class Item:
    pass


class MenuItem(Item):
    def __init__(self, title, lst, child=None):
        self.title = title
        self.lst = lst
        self.n = len(self.lst)
        self.i = 0
        self.child = child

    def next(self):
        self.i = (self.i + 1)%self.n

    def last(self):
        self.i = (self.i - 1)%self.n

    @property
    def cur(self):
        return self.lst[self.i]


class ChordItem(Item):
    def __init__(self, title, chord,  instrument, symble):
        self.title = title
        self.chord = chord
        self.instrument = instrument
        self.symble = symble


class BoardItem(Item):
    def __init__(self, root, title, strings, openstring):
        self.root = root
        self.title = title
        self.strings = strings
        self.openstring = openstring
