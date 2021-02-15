import random
import simpleaudio as sa
import pretty_midi

from random import uniform
import numpy as np

INSTRUMENTS = {
    '钢弦吉他': 'Acoustic Guitar(steel)',
    '尼龙吉他': 'Acoustic Guitar(nylon)',
    '原声钢琴': 'Acoustic Grand Piano',
    '马林巴琴': 'Marimba',
}

def generate_tone(semitones: int, t, fs: int = 44100, amplitude=1):
    result = np.array([])
    tone_frequency = int(440 * np.power(2**(1 / 12), semitones))
    size = int(t * fs)
    T = int(fs / tone_frequency)
    repeat_times = int(np.ceil(size / T))
    sample = np.array([uniform(-1, 1) for _ in range(T)])
    weight = 0.5
    for i in range(repeat_times):
        result = np.append(result, sample)
        sample = sample * weight + np.append(sample[-1],
                                             sample[:-1]) * (1 - weight)
    result = result[:size - 1]
    result = result * np.linspace(amplitude, 0.1, result.size)
    return result


def generate_chord(chord, duration, fs=44100, amp=1):
    for semitones in chord:
        t = duration
        result += generate_tone(semitones, t, fs, amp)
    result /= len(chord)
    result = result * (2**15 - 1) / np.max(np.abs(result))
    result = result.astype(np.int16)
    return result


def generate_song(song, beat_duration, fs=44100, amp=1):
    result = np.array([])
    for semitones, beats in song:
        t = beats * beat_duration
        result = np.append(result, generate_tone(semitones, t, fs, amp))
    result = result * (2**15 - 1) / np.max(np.abs(result))
    result = result.astype(np.int16)
    return result


def generate_song_by_fluidsynth(song, ration=0.2, instrument='尼龙吉他'):
    instrument = INSTRUMENTS[instrument]
    chord = pretty_midi.PrettyMIDI()
    program = pretty_midi.instrument_name_to_program(instrument)
    guitar = pretty_midi.Instrument(program=program)
    cur_time = 0
    for note_number, time in song:
        time *= ration
        note_number += 69
        note = pretty_midi.Note(velocity=random.randint(70, 100),
                                pitch=note_number,
                                start=cur_time,
                                end=cur_time + time)
        guitar.notes.append(note)
        cur_time += time
    chord.instruments.append(guitar)
    data = chord.fluidsynth()
    data = data * (2**15 - 1) / np.max(np.abs(data))
    data = np.int32(data)
    return data


def play(data, fs=44100):
    play_obj = sa.play_buffer(data, 1, 2, fs)
    play_obj.wait_done()


if __name__ == "__main__":
    song = [[3, 1], [5, 1], [3, 1], [3, .5], [5, .5],
            [10, 1], [10, 1], [10, .5], [7, .5], [5, .5], [7, .5], [5, 1],
            [3, 1], [3, 1], [3, .5], [5, .5], [5, 1], [3, 1], [3, 1], [-2, .5],
            [-2, .5]]

    data = generate_song_by_fluidsynth(song)
    play(data)
