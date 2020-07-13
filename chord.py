import logging
import pprint
from itertools import product
import re
from pprint import pprint 

import board
import scale

logging.basicConfig(level=logging.INFO)

# by interval of every two adjacent tone
CHORD_TYPES = {
    'M': [4, 3],
    'm': [3, 4],
    'M7': [4, 3, 4],
    'm7': [3, 4, 3],
    'm7-5': [3, 3, 4],
    'sus2': [2, 5],
    'sus4': [5, 2],
    'M9': [4, 3, 4, 3],
    'add9': [4, 3, 7],
}




class Chord(object):
    """Chord"""
    def __init__(self, **kw):
        """__init__

        :param **kw:
        """
        self.base = kw.get('base', 'G')
        self.type = kw.get('type', 'maj7')
        self.scales = []
        self.positions = []
        self._init()

        self.filters = {
            'OpenChords': 0,
            'Barrechord': 1,
            'inversion': 0,
            'gap': 5,
            'ignor': []
        }

    def _init(self):
        std_sca = list(scale.DIATONIC_SCALE)
        ind = std_sca.index(self.base)
        self.scales.append(self.base)
        for itv in CHORD_TYPES[self.type]:
            ind += itv
            if ind > 11:
                ind %= 12
            self.scales.append(std_sca[ind])

        strings = board.Board().strings
        inds = []
        for s_i, string in enumerate(strings):
            ind = []
            inds.append(ind)
            for i, s in enumerate(string):
                if s in self.scales:
                    ind.append((i, s,6 - s_i, ))
        # print('fuck')
        # print(inds)
        #  print(inds)
        self.positions = list(product(*inds))
        #  pprint(self.positions)


    def get_positions(self, **kw):
        """get_positions

        :param **kw:
        """
        ans = []

        filters = kw.get('filters', self.filters)
        # logging.info('开始过滤，过滤对象为：{0}{1} filters：{2}'.format(
            # self.base, self.type, filters))

        # positions = list(self.positions)
        # logging.info('初始个数为：' + str(len(self.positions)))

        strings = filters["strings"]
        for positions in self.positions:
            ps = []

            for string in strings:
                p = []
                for s in string:
                    p.append(positions[6 - s])
                ps.append(p)
            for p in ps:
                if filters['OpenChords']:
                    if min(p)[0] <= 0:
                        continue

                if filters['Barrechord']:
                    if min(p)[0] != 0:
                        continue

                gap = filters['gap']
                if gap:
                    if max(p)[0] - min(p, key=lambda i:
                                       (i[0] == 0, i[0]))[0] >= gap:
                        continue

                ignor = filters['ignor']
                if ignor is not None:

                    ignor = set(ignor)
                    scales = set(self.scales)
                    scales -= ignor
                    if set([val[1] for val in p]) != scales:
                        continue

                if filters['inversion']:
                    if p[0][1] != self.base:
                        continue
                if p not in ans:
                    ans.append(p)

        return ans


    def gen_wavg(self, file_name):
        """gen_wavg

        :param file_name:
        """
        pass


def find_equal(chord):
    scale = ['1', 'b2', '2', 'b3', '3', '4', 'b5', '5', 'b6', '6', 'b7', '7']
    str2int = lambda s: scale.index(s) + 1
    chord = tuple(map(str2int, chord.split(' ')))
    for tone in chord:
        new_chord = [t - tone + 1 for t in chord]
        new_chord = [t - 1 if t > 0 else t + 12 - 1 for t in new_chord]
        new_chord.sort()
        new_chord = [scale[t] for t in new_chord]
        print('{}:{}'.format(scale[tone - 1], new_chord))


def test_findchord():
    filters = {
        'OpenChords': 0,
        'Barrechord': 1,
        'inversion': 1,
        'strings': [
            [6, 5, 4, 3, 2, 1],
            [5, 4, 3, 2, 1],
            [4, 3, 2, 1],
        ],
        'gap': 4,
        'ignor': []
    }
    Cm9 = Chord(base='G', type='m7-5')
    pprint.pprint((Cm9.get_positions(filters=filters)))
    print(Cm9.scales)


def test_findequal():
    chord = '1 3 4 6 b7'
    find_equal(chord)


if __name__ == '__main__':
    find_equal('1 3 4 5 7')



