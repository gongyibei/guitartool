from src.guitar import scale
from src.guitar.scale import Scale
from src.guitar.tuning import TUNINGS


class Board(object):
    def __init__(self, tuning=TUNINGS['Stander']):
        """
        starts:a list of 6 str as the begin scale from 6th string to 1th string
        """
        self.tuning = tuning
        self.strings = self._get_strings()

    def _get_strings(self):
        sca = list(scale.DIATONIC_SCALE)
        strings = []
        for sta in self.tuning:
            ind = sca.index(sta)
            strings.append(sca[ind:] + sca[:ind])
        return strings

    def get_pitchs(self, key):
        i = Scale.note2index(key)
        map = dict(zip(Scale.allnotes[i - 1:] + Scale.allnotes[:i-1], Scale.allpitchs))
        pitchs = []
        for string in self.strings:
            pitch = []
            for note in string:
                pitch.append(map[note])
            pitchs.append(pitch)
        return pitchs



    def __repr__(self):
        return str(self.strings)



if __name__ == '__main__':
    print(Board())
