# -*- coding: utf-8 -*-
import heapq
from itertools import combinations

DIATONIC_SCALE = ('C', 'bD', 'D', 'bE', 'E', 'F', 'bG', 'G', 'bA', 'A', 'bB',
                  'B')
#INTVAL = (2, 2, 1, 2, 2, 2)
INTVAL = (2, 2, 3, 2, 2)

ALL_NOTES = ('A', 'bB', 'B', 'C', 'bD', 'D', 'bE', 'E', 'F', 'bG', 'G', 'bA')


def get_next_note(note):
    i = ALL_NOTES.index(note)
    i = (i + 1)%12
    return ALL_NOTES[i]

def get_last_note(note):
    i = ALL_NOTES.index(note)
    i = (i + 11)%12
    return ALL_NOTES[i]

class Scale():

    allpitchs = ('1', 'b2', '2', 'b3', '3', '4', 'b5', '5', 'b6', '6',
                     'b7', '7')
    allnotes = ('C', 'bD', 'D', 'bE', 'E', 'F', 'bG', 'G', 'bA','A', 'bB', 'B',)

    def __init__(self, pitchs, interval, en_name='unnamed', zh_name='unnamed'):

        self.pitchs = pitchs
        self.interval = interval
        self.en_name = en_name
        self.zh_name = zh_name

    @classmethod
    def pitch2index(cls, pitch):
        return {
            '1': 1,
            '#1': 2,
            'b2': 2,
            '2': 3,
            '#2': 4,
            'b3': 4,
            '3': 5,
            '4': 6,
            '#4': 7,
            'b5': 7,
            '5': 8,
            '#5': 9,
            'b6': 9,
            '6': 10,
            '#6': 11,
            'b7': 11,
            '7': 12
        }[pitch]
    @classmethod
    def note2index(cls,note):
        return {
            'C': 1,
            '#C': 2,
            'bD': 2,
            'D': 3,
            '#D': 4,
            'bE': 4,
            'E': 5,
            'F': 6,
            '#F': 7,
            'bG': 7,
            'G': 8,
            '#G': 9,
            'bA': 9,
            'A': 10,
            '#A': 11,
            'bB': 11,
            'B': 12
        }[note]

    
    @classmethod
    def frominterval(cls, interval, en_name='unnamed', zh_name='unnamed'):
        pitchs = ['1']
        ind = 0
        for i in interval:
            ind += i
            pitchs.append(cls.allpitchs[ind])
        pitchs = tuple(pitchs)
        return cls(pitchs, interval, en_name=en_name, zh_name=zh_name)

    @classmethod
    def frompitchs(cls, pitchs, en_name='unnamed', zh_name='unnamed'):
        interval = []
        lastind = 0
        for pitch in pitchs[1:]:
            curind = cls.pitch2index(pitch)
            interval.append(curind - lastind)
            lastind = curind
        interval = tuple(interval)
        return cls(pitchs, interval, en_name=en_name, zh_name=zh_name)

    def notes(self, key):
        sta = self.allnoteindex[key]-1
        allnotes = Scale.allnotes[sta:]+Scale.allnotes[:sta]
        pitchindex = tuple(self.pitch2index[pitch] for pitch in self.pitchs)
        return tuple(allnotes[i-1] for i in pitchindex)



class CommonScale():

    Ionian = Scale.frompitchs(('1', '2', '3', '4', '5', '6', '7'),
                              en_name='Ionian',
                              zh_name='自然大调音阶')
    Blues = Scale.frompitchs(('1', 'b3', '4', 'b5', '5', 'b7'),
                             en_name='Blues',
                             zh_name='布鲁斯音阶')
    Dorian = Scale.frompitchs(('1', '2', 'b3', '4', '5', '6', 'b7'),
                              en_name='Dorian',
                              zh_name='多里安音阶')
    Phrygian = Scale.frompitchs(('1', 'b2', 'b3', '4', '5', '#5', 'b7'),
                                en_name='Phrygian',
                                zh_name='弗里几亚音阶')
    Lydian = Scale.frompitchs(('1', '2', '3', 'b5', '5', '6', '7'),
                              en_name='Lydian',
                              zh_name='利底亚音阶')
    Mixolydian = Scale.frompitchs(('1', '2', '3', '4', '5', '6', 'b7'),
                                  en_name='Mixolydian',
                                  zh_name='混合利底亚音阶')
    Aeolian = Scale.frompitchs(('1', '2', 'b3', '4', '5', '#5', 'b7'),
                               en_name='Aeolian',
                               zh_name='自然小调音阶')
    Locrian = Scale.frompitchs(('1', 'b2', 'b3', '4', 'b5', '#5', 'b7'),
                               en_name='Locrian',
                               zh_name='洛克里亚音阶')
    Diminished_H_W = Scale.frompitchs(
        ('1', 'b2', 'b3', '3', 'b5', '5', '6', 'b7'),
        en_name='Diminished H-W',
        zh_name='减音阶')
    Diminished_W_H = Scale.frompitchs(
        ('1', '2', 'b3', '4', 'b5', '#5', '6', '7'),
        en_name='Diminished W-H',
        zh_name='减音阶')
    Whole_Tone = Scale.frompitchs(('1', '2', '3', 'b5', '#5', 'b7'),
                                  en_name='Whole Tone',
                                  zh_name='全音音阶')
    Melodic_Minor = Scale.frompitchs(('1', '2', 'b3', '4', '5', '6', '7'),
                                     en_name='Melodic Minor',
                                     zh_name='曲调小音阶')
    Dorian_b2 = Scale.frompitchs(('1', 'b2', 'b3', '4', '5', '6', 'b7'),
                                 en_name='Dorian b2',
                                 zh_name='b2多里安音阶')
    Lydian_Aug = Scale.frompitchs(('1', '2', '3', 'b5', '#5', '6', '7'),
                                  en_name='Lydian Aug',
                                  zh_name='增利底亚音阶')
    Lydian_b7 = Scale.frompitchs(('1', '2', '3', 'b5', '5', '6', 'b7'),
                                 en_name='Lydian b7',
                                 zh_name='b7利底亚音阶')
    Mixolydian_b6 = Scale.frompitchs(('1', '2', '3', '4', '5', '#5', 'b7'),
                                     en_name='Mixolydian b6',
                                     zh_name='b6混合利底亚音阶')
    Locrian_2 = Scale.frompitchs(('1', '2', 'b3', '4', 'b5', '#5', 'b7'),
                                 en_name='Locrian 2',
                                 zh_name='2洛克里亚音阶')
    Altered = Scale.frompitchs(('1', 'b2', 'b3', '3', 'b5', '#5', 'b7'),
                               en_name='Altered',
                               zh_name='变形音阶')
    Harmonic_Minor = Scale.frompitchs(('1', '2', 'b3', '4', '5', '#5', '7'),
                                      en_name='Harmonic Minor',
                                      zh_name='和声小调音阶')
    Locrian_6 = Scale.frompitchs(('1', 'b2', 'b3', '4', 'b5', '6', 'b7'),
                                 en_name='Locrian 6',
                                 zh_name='6洛克里亚音阶')
    Ionian_Aug = Scale.frompitchs(('1', '2', '3', '4', '#5', '6', '7'),
                                  en_name='Ionian Aug',
                                  zh_name='增伊欧尼安音阶')
    Dorian_sharp4 = Scale.frompitchs(('1', '2', 'b3', 'b5', '5', '6', 'b7'),
                                     en_name='Dorian #4',
                                     zh_name='#4多里安音阶')
    Phrygian_Major = Scale.frompitchs(('1', 'b2', '3', '4', '5', '#5', 'b7'),
                                      en_name='Phrygian Major',
                                      zh_name='大弗里几亚音阶')
    Lydian_sharp9 = Scale.frompitchs(('1', 'b3', '3', 'b5', '5', '6', '7'),
                                     en_name='Lydian #9',
                                     zh_name='#9利底亚音阶')
    Altered_bb7 = Scale.frompitchs(('1', 'b2', 'b3', '3', 'b5', '#5', '6'),
                                   en_name='Altered bb7',
                                   zh_name='b7变形音阶')
    Pentanote_Major = Scale.frompitchs(('1', '2', '3', '5', '6'),
                                       en_name='Pentanote Major',
                                       zh_name='大调五声音阶')
    Pentanote_Minor = Scale.frompitchs(('1', 'b3', '4', '5', 'b7'),
                                       en_name='Pentanote Minor',
                                       zh_name='小调五声音阶')
    Augmented = Scale.frompitchs(('1', '1', '3', '5', '#5', '7'),
                                 en_name='Augmented',
                                 zh_name='增音阶')
    Arabian = Scale.frompitchs(('1', '2', '3', '4', 'b5', '#5', 'b7'),
                               en_name='Arabian',
                               zh_name='阿拉伯音阶')
    Balinese = Scale.frompitchs(('1', 'b2', 'b3', '5', '#5'),
                                en_name='Balinese',
                                zh_name='巴里音阶')
    Byzantine = Scale.frompitchs(('1', 'b2', '3', '4', '5', '#5', '7'),
                                 en_name='Byzantine',
                                 zh_name='拜占庭音阶')
    Chinese = Scale.frompitchs(('1', '3', 'b5', '5', '7'),
                               en_name='Chinese',
                               zh_name='中国音阶')
    Chinese_Mongolian = Scale.frompitchs(('1', '2', '3', '5', '6'),
                                         en_name='Chinese Mongolian',
                                         zh_name='中国蒙古音阶')
    Double_Harmonic = Scale.frompitchs(('1', 'b2', '3', '4', '5', '#5', '7'),
                                       en_name='Double Harmonic',
                                       zh_name='双和声音阶')
    Egyptian = Scale.frompitchs(('1', '2', '4', '5', 'b7'),
                                en_name='Egyptian',
                                zh_name='埃及音阶')
    Eight_Tone_Spanish = Scale.frompitchs(
        ('1', 'b2', 'b2', '3', '4', 'b5', '#5', 'b7'),
        en_name='Eight Tone Spanish',
        zh_name='西班牙8度音阶')
    Enigmatic = Scale.frompitchs(('1', 'b2', '3', 'b5', '#5', 'b7', '7'),
                                 en_name='Enigmatic',
                                 zh_name='神秘音阶')
    Hindu = Scale.frompitchs(('1', '2', '3', '4', '5', '#5', 'b7'),
                             en_name='Hindu',
                             zh_name='印度音阶')
    Hirajoshi = Scale.frompitchs(('1', '2', 'b3', '5', '#5'),
                                 en_name='Hirajoshi',
                                 zh_name='日本音阶')
    Hungarian_Major = Scale.frompitchs(('1', 'b3', '3', 'b5', '5', '6', 'b7'),
                                       en_name='Hungarian Major',
                                       zh_name='匈牙利大调音阶')
    Hungarian_Minor = Scale.frompitchs(('1', '2', 'b3', 'b5', '5', '#5', '7'),
                                       en_name='Hungarian Minor',
                                       zh_name='匈牙利小调音阶')
    Hungarian_Gypsy = Scale.frompitchs(('1', '2', 'b3', 'b5', '5', '#5', '7'),
                                       en_name='Hungarian Gypsy',
                                       zh_name='匈牙利吉卜赛音阶')
    Ichikosucho = Scale.frompitchs(('1', '2', '3', '4', 'b5', '5', '6', '7'),
                                   en_name='Ichikosucho',
                                   zh_name='日本音阶')
    Kumoi = Scale.frompitchs(('1', '2', 'b3', '5', '6'),
                             en_name='Kumoi',
                             zh_name='岩上音阶')
    Leading_Whole_Tone = Scale.frompitchs(
        ('1', '2', '3', 'b5', '#5', 'b7', '7'),
        en_name='Leading Whole Tone',
        zh_name='主要全音阶')
    Lydian_Diminished = Scale.frompitchs(('1', '2', 'b3', 'b5', '5', '6', '7'),
                                         en_name='Lydian Diminished',
                                         zh_name='减利底亚音阶')
    Lydian_Minor = Scale.frompitchs(('1', '2', '3', 'b5', '5', '#5', 'b7'),
                                    en_name='Lydian Minor',
                                    zh_name='小利底亚音阶')
    Mohammedan = Scale.frompitchs(('1', '2', 'b3', '4', '5', '#5', '7'),
                                  en_name='Mohammedan',
                                  zh_name='伊斯兰音阶')
    Neopolitan = Scale.frompitchs(('1', 'b2', 'b3', '4', '5', '#5', '7'),
                                  en_name='Neopolitan',
                                  zh_name='拿波里音阶')
    Neopolitan_Major = Scale.frompitchs(('1', 'b2', 'b3', '4', '5', '6', '7'),
                                        en_name='Neopolitan Major',
                                        zh_name='大拿波里音阶')
    Neopolitan_Minor = Scale.frompitchs(
        ('1', 'b2', 'b3', '4', '5', '#5', 'b7'),
        en_name='Neopolitan Minor',
        zh_name='小拿波里音阶')
    Overtone = Scale.frompitchs(('1', '2', '3', 'b5', '5', '6', 'b7'),
                                en_name='Overtone',
                                zh_name='泛音音阶')
    Pelog = Scale.frompitchs(('1', 'b2', 'b3', '5', '#5'),
                             en_name='Pelog',
                             zh_name='印尼音阶')
    Persian = Scale.frompitchs(('1', 'b2', '3', '4', 'b5', '#5', '7'),
                               en_name='Persian',
                               zh_name='波斯音阶')
    Prometheus = Scale.frompitchs(('1', '2', '3', 'b5', '6', 'b7'),
                                  en_name='Prometheus',
                                  zh_name='希腊音阶')
    Prometheus_Neopolitan = Scale.frompitchs(('1', 'b2', '3', 'b5', '6', 'b7'),
                                             en_name='Prometheus Neopolitan',
                                             zh_name='拿波里希腊音阶')
    Purvi_Theta = Scale.frompitchs(('1', 'b2', '3', 'b5', '5', '#5', '7'),
                                   en_name='Purvi Theta',
                                   zh_name='印度布尔维音阶')
    Six_Tone_Symmetrical = Scale.frompitchs(('1', 'b2', '3', '4', '#5', '6'),
                                            en_name='Six Tone Symmetrical',
                                            zh_name='对称6度音阶')
    Todi_Theta = Scale.frompitchs(('1', 'b2', 'b3', 'b5', '5', '#5', '7'),
                                  en_name='Todi Theta',
                                  zh_name='印度陶笛音阶')


def special():
    """special
    计算能确定一个调的所有音的可能的集合
    """
    major_scales = []
    for ind, main in enumerate(DIATONIC_SCALE):
        scale = DIATONIC_SCALE[ind:] + DIATONIC_SCALE[:ind]
        major_scale = []
        major_scales.append(major_scale)
        i = 0
        major_scale.append(scale[0])
        for itv in INTVAL:
            i += itv
            major_scale.append(scale[i])
    for scale in major_scales:
        s = scale[0]
        main = [s + ' ', s][len(s) == 2]
        # print(main + ' 调: ' + '  '.join([s + ' ', s][len(s) == 2] for s in scale))
    out = []
    for i in range(7):
        for subset in combinations(major_scales[0], i):
            for superset in major_scales[1:]:
                subset = set(subset)
                if subset.issubset(set(superset)):
                    break
            else:
                out.append(subset)
    out = [sorted(s, key=lambda i: DIATONIC_SCALE.index(i)) for s in out]
    return out

if __name__ == '__main__':
    print(CommonScale.Ionian.pitchs)

