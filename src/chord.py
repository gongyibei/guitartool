import logging
import re
from itertools import product
import tuning

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


class Chord():
    TYPES = [ 'M', 'm', 'M7', 'm7', 'm7-5', 'sus2', 'sus4', 'M9', 'add9']
    def __init__(self, base, type):
        self.base = base
        self.type = type
        self.name = f'{base}{type}'
        self.interval = self.get_interval(type)

        self.pitchs = []


    @classmethod
    def get_interval(cls, type):
        return {
            'M': [4, 3],
            'm': [3, 4],
            'M7': [4, 3, 4],
            'm7': [3, 4, 3],
            'm7-5': [3, 3, 4],
            'sus2': [2, 5],
            'sus4': [5, 2],
            'M9': [4, 3, 4, 3],
            'add9': [4, 3, 7],
        }.get(type, None)

    def get_guitar_chords(self, tuning):
        std_scale = list(scale.DIATONIC_SCALE)
        ind = std_sca.index(self.base)
        self.scales.append(self.base)
        for itv in self.interval:
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
                    ind.append((
                        i,
                        s,
                        6 - s_i,
                    ))
        self.positions = list(product(*inds))
        pass




def get_chords(base, type, instrument='guitar') :
    chords = []

    if instrument == 'guitar':
        n_string = 6
    elif instrument == 'ukelele':
        n_string = 4
    else:
        raise Exception('Unsupported instrument!')
        







class GuitarChord():
    def __init__(self, base, type, notes, tuning=tuning.GuitarTuning.STANDARD):
        super().__init__(base, type, tuning)
        self.n_string = len(tuning)
        self.tuning = tuning
        self.inversion = 0

        self.notes = []
        self.frets = []

    def get_chords(self):
        pass

    def play(self):
        pass

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
                    ind.append((
                        i,
                        s,
                        6 - s_i,
                    ))
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

if __name__ == '__main__':
    pass

