#-*- coding: utf-8 -*-

import numpy as np
from scipy.io.wavfile import write
from functools import reduce
import random
import simpleaudio as sa

from random import uniform
import numpy as np


class Tone:
    a1 = 440  # 标准音a1
    r = np.power(2, 1 / 12)  # 12平均律的比值


def generate_tone(semitones: int, t, fs: int = 44100, amplitude=1):
    """
    :param semitones: 与标准音相差的半音数
    :param t:         该音调持续的时长
    :param fs:        采样频率
    :param amplitude: 最大振幅，用于调节音量
    :return: 该音调的采样信号
    """
    result = np.array([])

    # 1. some instants
    tone_frequency = int(Tone.a1 * np.power(Tone.r, semitones))  # 该音调的频率
    size = int(t * fs)  # 总的采样点个数
    T = int(fs / tone_frequency)  # 一个周期的采样点个数
    repeat_times = int(np.ceil(size / T))  # 在时间 t 内，循环的次数

    # 2. generate random wav with the length T
    sample = np.array([uniform(-1, 1) for _ in range(T)])

    # use the synthesis algorithm
    weight = 0.5
    for i in range(repeat_times):
        result = np.append(result, sample)
        sample = sample * weight + np.append(sample[-1], sample[:-1]) * (
            1 - weight)  # 这便是算法的核心。。

    result = result[:size - 1]  # 裁减多余的部分
    result = result * np.linspace(
        amplitude, 0.1, result.size)  # 渐弱处理，使音调之间能平滑过渡。同时最大振幅设为 amplitude

    return result


def generate_chord(chord, chord_duration, fs=44100, amplitude=1):
    for semitones in chord:
        t = chord_duration
        result = generate_tone(semitones, t, fs, amplitude)
    result /= len(chord)

    result = result * (2**15 - 1) / np.max(np.abs(result))
    result = result.astype(np.int16)
    return result


def generate_song(song, beat_duration, fs=44100, amplitude=1):
    result = np.array([])
    for semitones, beats in song:
        t = beats * beat_duration
        result = np.append(result, generate_tone(semitones, t, fs, amplitude))

    result = result * (2**15 - 1) / np.max(np.abs(result))
    result = result.astype(np.int16)
    return result


def play(data, fs=44100):
    play_obj = sa.play_buffer(data, 1, 2, fs)
    play_obj.wait_done()


if __name__ == "__main__":
    song = [[3, 1], [5, 1], [3, 1], [3, .5], [5, .5],
            [10, 1], [10, 1], [10, .5], [7, .5], [5, .5], [7, .5], [5, 1],
            [3, 1], [3, 1], [3, .5], [5, .5], [5, 1], [3, 1], [3, 1], [-2, .5],
            [-2, .5]]

    data = generate_song(song, 0.4)
    play(data)
