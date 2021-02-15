import logging
from itertools import product

from src.guitar import scale
from src.guitar.board import Board
from src.guitar.scale import DIATONIC_SCALE
from src.guitar.tuning import TUNINGS

logging.basicConfig(level=logging.INFO)

# By interval of every two adjacent tone
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
    def __init__(self, base, type, tuning):
        """__init__
        :param **kw:
        """
        self.base = base
        self.type = type
        self.tuning = TUNINGS[tuning]
        self.notes = []
        self.pitchs = []
        self.intervals = []
        self.scales = []
        self.positions = []
        self._init()

        self.filters = {
            'openchords': 0,
            'barrechord': 1,
            'inversion': 0,
            'gap': 5,
            'ignore': []
        }

    def _init(self):
        std_sca = list(DIATONIC_SCALE)
        ind = std_sca.index(self.base)
        self.scales.append(self.base)
        for itv in CHORD_TYPES[self.type]:
            ind += itv
            if ind > 11:
                ind %= 12
            self.scales.append(std_sca[ind])

        strings = Board(self.tuning).strings
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
        strings = filters["strings"]
        for positions in self.positions:
            ps = []
            for string in strings:
                p = []
                for s in string:
                    p.append(positions[6 - s])
                ps.append(p)
            for p in ps:
                if filters['openchords']:
                    if min(p)[0] <= 0:
                        continue
                if filters['barrechord']:
                    if min(p)[0] != 0:
                        continue
                gap = filters['gap']
                if gap:
                    if max(p)[0] - min(p, key=lambda i:
                    (i[0] == 0, i[0]))[0] >= gap:
                        continue

                ignore = filters['ignore']
                if ignore is not None:

                    ignore = set(ignore)
                    scales = set(self.scales)
                    scales -= ignore
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
