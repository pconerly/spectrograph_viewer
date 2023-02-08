# manual notebook
from __future__ import print_function

import simplejson
import os
import collections

import numpy as np
import librosa
import time

# from export_mp3 import export_mp3
# from spikes.analysis.export_ogg import export_ogg

from librosa.decompose import decompose
from librosa import fft_frequencies, mel_frequencies

PROJECT_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'output')


def pdesc(arr, desc='array'):

    if len(arr) > 0 and isinstance(arr[0], (collections.Sequence, np.ndarray)):
        print('Size of %s: %s by %s' % (desc, len(arr), len(arr[0])))
    else:
        print('Size of %s: %s' % (desc, len(arr)))


def grabfile(filename):

    audio_path = os.path.join(PROJECT_DIR, filename)

    y, sr = librosa.load(audio_path, sr=None)
    print('Sampling rate? %s' % sr)

    pdesc(y, 'source audio')
    # print("Size of the source audio: %s by %s" % (len(y), 'what'))
    return y, sr


def mel_fs(n_mels=256, fmin=9, fmax=None, htk=False, sr=44100):

    np.set_printoptions(precision=3, threshold=1500)
    if fmax is None:
        fmax = sr / 2
    mel_f = mel_frequencies(n_mels + 2, fmin=fmin, fmax=fmax, htk=htk)
    pdesc(mel_f, 'mel_f')
    print(mel_f)
    print("-----")

    f = np.vectorize(
        librosa.hz_to_midi
    )  # or use a different name if you want to keep the original f

    result_array = f(mel_f)  # if A is your Numpy array
    print(result_array)


def generate_spectrogram_timetable(y, sr):
    # If we're doing 1024 frequency samples by 86 steps per second, then we should have more information than 44100hz

    results = []
    mel_intervals = [1024]
    hopl_intervals = [64]
    for mel in mel_intervals:
        for hopl in hopl_intervals:
            start = time.time()
            S = librosa.feature.melspectrogram(y,
                                               sr=sr,
                                               n_mels=mel,
                                               hop_length=hopl)
            results.append([mel, hopl, time.time() - start, len(S), len(S[0])])

    print("Mels: \tHops: \ttime:")
    for r in results:
        print("%s\t%s\t%s\tsize: %sx%s" % (r[0], r[1], r[2], r[3], r[4]))


def identify_complex_note():
    pass
    # for each frame
    # identify local maxima
    # identify the true Hz based off of the parabola-sampling thingy algorithm
    # see if the Hz are overtones/undertones of eachother


def generate_spectrogram(y, sr, n_mels=1024, hop_l=512, n_fft=2048):
    # Let's make and display a mel-scaled power (energy-squared) spectrogram
    # hop_l = 64
    # hop_l = 512

    S = librosa.feature.melspectrogram(y,
                                       sr=sr,
                                       n_mels=n_mels,
                                       hop_length=hop_l,
                                       n_fft=n_fft)
    # hop length: 512 -> 3.89 seconds
    # 256 -> 6.67
    # 128 -> 13 seconds

    # I should probably save this for later?

    pdesc(S, 'spectrogram')
    return (S, sr)


def convert_to_log(S):
    # Convert to log scale (dB). We'll use the peak power as reference.
    # log_S = librosa.amplitude_to_db(S, ref_power=np.max)
    log_S = librosa.amplitude_to_db(S, ref=np.max)
    pdesc(log_S, 'log spectrogram')
    return log_S


def main(S, sr):
    (components, activations) = decompose(S)

    pdesc(components, 'components')
    pdesc(activations, 'activations')

    # re-create the new S
    undecomposed_S = components.dot(activations)

    pdesc(undecomposed_S, 'de-decomposed_S')

    # export_mp3(undecomposed_S, 'treetop_undecomposed')
    # export_ogg(undecomposed_S, 'treetop_undecomposed')
    # export_ogg(y, 'derp', sr=sr)

    # write it to mp3 or .wav


def form_json(nparr, **kwargs):
    data = {
        'data': nparr.tolist(),
    }
    data.update(kwargs)
    print("our keys are: %s" % data.keys())
    json_data = simplejson.dumps(data, separators=(',', ':'))
    return json_data


def write_to_json(filename, nparr, **kwargs):
    dest = os.path.join(OUTPUT_DIR, "%s.json" % filename)
    with open(dest, 'w') as fout:
        json_data = form_json(nparr, **kwargs)
        fout.write(json_data)


def findMinMax(arr):
    curMin = 0
    curMax = 0

    for row in arr:
        for item in row:
            curMax = max(curMax, item)
            curMin = min(curMin, item)

    print("curMax: %s" % curMax)
    print("curMin: %s" % curMin)


def find_maxes(log_S, f_mels):
    # for each log_S column
    # iterate through values
    # if we found a max, do a curve analysis

    note_pieces = []
    # I may need to figure out a way to record a threshold

    for t in range(len(log_S[0])):
        # print('whats t: %s' % t)
        # we're in a new timestamp
        # for f in range(len(log_S)):
        #     pass
        localmaxes = librosa.util.localmax(log_S[:, t])
        for index, lmax in enumerate(localmaxes):
            # print(lmax)
            if lmax:
                note_pieces.append((f_mels[index], t))
    # print('note_pieces')
    # print(note_pieces)
    print('len of note_pieces %s' % len(note_pieces))
    return note_pieces


def gen_spectrograph_and_save(filename,
                              save=False,
                              special_export=False,
                              get_json=False):
    n_mels = 370
    hop_l = 512
    # n_fft=2048 <-- a librosa default
    y, sr = grabfile(filename)
    S, sr = generate_spectrogram(y, sr, n_mels=n_mels, hop_l=hop_l)
    log_S = convert_to_log(S)

    f_mels = mel_frequencies(n_mels).tolist()

    note_pieces = find_maxes(log_S, f_mels)
    if special_export:
        # log_S[:80].tofile('out_80.txt')
        print('Shape of special output: %s' % (S[:, 80].shape))
        S[:, 80].tofile('first_80.txt')

    log_S = np.swapaxes(log_S, 0, 1)
    x_length = len(log_S)
    data_obj = {
        'n_mels': n_mels,
        'f_mels': f_mels,
        'hop_l': hop_l,
        'x_length': x_length,
        'y_length': len(log_S[0]),
        'note_pieces': note_pieces,
        'sr': sr,
        'duration': x_length * (hop_l / sr),
    }
    if save:
        write_to_json(filename, log_S, **data_obj)

    if get_json:
        json_data = form_json(log_S, **data_obj)
        return json_data
    return (log_S, data_obj)


if __name__ == '__main__':
    start = time.time()

    filename = 'treetop_01_intro.mp3'
    # gen_spectrograph_and_save(filename, save=True)

    gen_spectrograph_and_save(filename, special_export=True)
    # gen_spectrograph_and_save(filename)

    # mel_fs()
    # y, sr = grabfile(filename)
    # generate_spectrogram_timetable(y, sr)
    # S, sr = generate_spectrogram(y, sr)
    # log_S = convert_to_log(S)

    # mel_fs(n_mels=1024)
    # S = generate_spectrogram(y, sr)
    # main(S, sr)
    print('Finished in %s seconds' % (time.time() - start))
