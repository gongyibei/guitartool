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
    b = Board(tuning.STANDER)
    print(b)
    place = ['52','32','43','23']

    # chord = '''
                  # {}
      # ×\033[1;34m┌───11───┬───12───┬───13───┐\033[0m
       # \033[1;34m├───21───┼───22───┼───23───┤\033[0m
       # \033[1;34m├───31───┼───32───┼───33───┤\033[0m
       # \033[1;34m├───41───┼───42───┼───43───┤\033[0m
       # \033[1;34m├───51───┼───52───┼───53───┤\033[0m
      # ×\033[1;34m└───61───┴───62───┴───63───┘\033[0m
           # 1st
    # '''.format('\033[1;35mBm7-5\033[0m')
    chord = '''
                  {}
      ×\033[1;34m┏───11───┬───12───┬───13───┐\033[0m
       \033[1;34m┣───21───┼───22───┼───23───┤\033[0m
       \033[1;34m┣───31───┼───32───┼───33───┤\033[0m
       \033[1;34m┣───41───┼───42───┼───43───┤\033[0m
       \033[1;34m┣───51───┼───52───┼───53───┤\033[0m
      ×\033[1;34m┗───61───┴───62───┴───63───┘\033[0m
           1st
    '''.format('\033[1;35mBm7-5\033[0m')
    # .format('\033[1;35m① \033[0m','\033[1;35m② \033[0m','\033[1;35m③ \033[0m')
    for p in place:
        chord = chord.replace('─'+p,'─\033[0m\033[1;35m♬ \033[0m\033[1;34m')
    chord = re.sub('─\d\d','───' ,chord)

    print(chord)
