import math
import random
import re
from enum import Enum, unique

from chord import Chord

class Color:
    black = '30'
    red = '31'
    green = '32'
    yellow = '33'
    blue = '34'
    purple = '35'
    cyanine = '36'
    white = '37'
    # b_blue = '44'
    # black = '90'
    # red = '91'
    # green = '92'
    # yellow = '93'
    # blue = '94'
    # purple = '95'
    # cyanine = '96'
    # white = '97'

    @classmethod
    def colortext(cls, color, text):
        return '\033[1;{}m{}\033[0m'.format(color, text)

    @classmethod
    def embed_colortext(cls, color, origincolor, text):
        return '\033[0m\033[1;{}m{}\033[0m\033[1;{}m'.format(
            color, text, origincolor)

    @classmethod
    def test(cls):
        origin = cls.colortext(cls.black, 'I {} you')
        embed = cls.embed_colortext(cls.cyanine, cls.black, 'fuck')
        ultimate = origin.format(embed)
        print(ultimate)

    @classmethod
    def test_allcolor(cls, text):
        print('\033[1;{}m{}\033[0m'.format(cls.black, text))
        print('\033[1;{}m{}\033[0m'.format(cls.red, text))
        print('\033[1;{}m{}\033[0m'.format(cls.green, text))
        print('\033[1;{}m{}\033[0m'.format(cls.yellow, text))
        print('\033[1;{}m{}\033[0m'.format(cls.blue, text))
        print('\033[1;{}m{}\033[0m'.format(cls.purple, text))
        print('\033[1;{}m{}\033[0m'.format(cls.cyanine, text))
        print('\033[1;{}m{}\033[0m'.format(cls.white, text))


class Pattern:
    def __init__(self, pattern_type, **config):
        '''
        Args:
            pattern_type: 'guitar' or 'ukelele'
            config: {
                'title_color' : Color.purple
                'board_color' : Color.blue
                'left_color' : Color.black
                'right_color' : Color.black
                'bottom_color': Color.yellow
                'press_position_color' : Color.purple
                'pitch_color' : Color.purple
            }
        '''
        self.pattern_type = pattern_type
        self.nstring = {'guitar': 6, 'ukelele': 4}[self.pattern_type]

        self.forbid = config.get('forbid', Color.red)
        self.pitch_color = config.get('pitch_color', Color.purple)
        self.title_color = config.get('title_color', '104')
        self.board_color = config.get('board_color', '94')
        self.left_color = config.get('left_color', Color.red)
        self.right_color = config.get('right_color', Color.cyanine)
        self.bottom_color = config.get('bottom_color', Color.yellow)
        self.press_position_color = config.get('press_position_color',
                                               Color.purple)

    def draw(self):
        pass


class ChordPattern(Pattern):
    def __init__(self, pattern_type, **config):
        super(ChordPattern, self).__init__(pattern_type, **config)
        # self.pattern = self.__render()
        ['🔈', '🔉', '🔊']
        self.press_position_symbles = ['🌈', '🐶', '🌀']
        #  self.press_position_symbles = ['🔈', '🔉', '🔊']
        #  self.press_position_symbles = ['1️⃣ ', '2️⃣ ', '3️⃣ ']

    def draw(self, title, n, chords):
        '''
        Args:
            title: the title of the chord
            n: number of chords printed in one row
            chords: press positions of chords
        '''
        cnt = 0
        text = [''] * (self.nstring + 2)
        for chord in chords:
            chord = [(p[2], p[0], p[1]) for p in chord]
            cnt += 1
            for i, line in enumerate(self.chord2text(title, chord)):
                text[i] += ' ' + line + ' '
            if cnt == n:
                print('\n'.join(text))
                print('\n\n')
                cnt = 0
                text = [''] * (self.nstring + 2)
        if cnt > 0:
            print('\n'.join(text))
            print('\n\n')

    def chord2text(self, title, chord):
        '''
        Args:
            title: the title of chord
        '''
        string_colors = [self.forbid] * self.nstring
        positions = chord
        minfret = min(chord, key=lambda p: p[1] if p[1] != 0 else 100)[1]
        maxfret = max(chord, key=lambda p: p[1])[1]
        minfret = min(maxfret - 2, minfret)
        minfret = max(minfret, 1)
        nfret = maxfret - minfret + 1
        nfret = max(nfret, 3)
        filling = [['──'] * nfret for _ in range(self.nstring)]

        width = 32
        if nfret > 3:
            right_width = 2
            board_width = 29
            half_fret_width = 3
        else:
            right_width = 3
            board_width = 28
            half_fret_width = 4

        left_width = 1

        right = [' ' * right_width] * self.nstring
        left = [Color.colortext(self.left_color, '×')] * self.nstring
        press_position = random.choice(self.press_position_symbles)

        for position in positions:
            string = position[0]
            fret = position[1]
            content = position[2]

            string_colors[string - 1] = self.board_color
            if fret == 0:
                left[string - 1] = Color.colortext(self.left_color, '○')
            else:
                left[string - 1] = ' '
                press_position = Color.colortext(self.press_position_color,
                                                 press_position)
                filling[string - 1][fret - minfret] = press_position

            right[string - 1] = Color.colortext(self.right_color,
                                                content.ljust(right_width))
        for i in range(self.nstring):
            string_color = string_colors[i]
            for j in range(nfret):
                if filling[i][j] == '──':
                    filling[i][j] = Color.colortext(string_color, '──')
        text = []
        side_width = board_width - len(title) - 2
        bleft_width = int(side_width / 2)
        bright_width = math.ceil(side_width / 2)

        title = ' ' * (bleft_width + left_width) + Color.colortext(
            self.title_color,
            ' {} '.format(title)) + ' ' * (bright_width + right_width)

        text.append(title)

        strings = self.__render_strings(left, right, string_colors, filling)
        text.extend(strings)

        bleft_width = left_width + half_fret_width
        bright_width = width - bleft_width - 2
        extra = 0
        if minfret < 10:
            extra = 1

        bottom = ' ' * (bleft_width) + Color.colortext(
            self.bottom_color, minfret) + ' ' * (bright_width + extra)

        text.append(bottom)
        return text

    def __render_strings(self, left, right, string_colors, filling):
        '''
        Args:
            left: colored
            right: colored
            string_color: every
        '''

        nfret = len(filling[0])

        strings = []

        if nfret > 3:
            line = '──'
        else:
            line = '───'

        for n in range(self.nstring):

            string_color = string_colors[n]
            if n == 0:
                l = Color.colortext(string_color, '┏' + line)
                joint = Color.colortext(string_color, line + '┬' + line)
                r = Color.colortext(string_color, line + '┐')
            elif n != self.nstring - 1:
                l = Color.colortext(string_color, '┣' + line)
                joint = Color.colortext(string_color, line + '┼' + line)
                r = Color.colortext(string_color, line + '┤')
            else:
                l = Color.colortext(string_color, '┗' + line)
                joint = Color.colortext(string_color, line + '┴' + line)
                r = Color.colortext(string_color, line + '┘')

            string = left[n] + l + joint.join(filling[n]) + r + right[n]
            strings.append(string)

        return strings


def test_draw():
    filters = {
        'OpenChords':
        0,
        'Barrechord':
        0,
        'inversion':
        1,
        'strings': [
            [6, 5, 4, 3, 2, 1],
            [5, 4, 3, 2, 1],
            [4, 3, 2, 1],
            [6, 4, 3, 2],
            [5, 4, 3, 2],
        ],
        'gap':
        4,
        'ignor': []
    }
    Cm9 = Chord(base='C', type='M')
    chords = Cm9.get_positions(filters=filters)
    #  print(chords)
    #  chords = list(set(chords))
    chords.sort(
        key=lambda c: min(c, key=lambda p: p[0] if p[0] != 0 else 100)[0])

    cp = ChordPattern('guitar')
    cp.draw('C', 4, chords)


if __name__ == '__main__':
    print('\n')
    test_draw()
