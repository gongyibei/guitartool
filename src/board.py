import pprint

import scale
import tuning
import re


class Board(object):
    def __init__(self, tuning=tuning.STANDER):
        '''
        starts:a list of 6 str as the begin scale from 6th string to 1th string  
        '''

        self.strings = self._get_strings(tuning)

    def _get_strings(self, tuning):
        sca = list(scale.DIATONIC_SCALE)
        strings = []
        for sta in tuning:
            ind = sca.index(sta)
            strings.append(sca[ind:] + sca[:ind])
        return strings

    def __repr__(self):
        return str(self.strings)
if __name__ == '__main__':
    print(Board())
