import os
import librosa
from librosa import (fft_frequencies, mel_frequencies,
                                         hz_to_midi)
# from .rose import _spectrogram as spectrogram
from rose import _spectrogram as spectrogram

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def test_spectrogram():
    # load our sound file
    # try doing spectogram on one part
    pass
    # print('PROJECT_DIR', PROJECT_DIR)
    fp = 'treetop_01_intro.mp3'

    audio_path = os.path.join(PROJECT_DIR, fp)

    y, sr = librosa.load(audio_path, sr=None)
    # print('Sampling rate? %s' % sr)

    hopl = 64
    intervals = 1024
    # intervals = 1024
    S = spectrogram(y, hop_length=hopl)  #, n_fft=intervals)

    # print('--------')
    # print('Whats S')
    # print(S)
    # # print(S[80])
    (a, b) = S
    # print(len(S))

    print('--------')
    print(a[80])

    print('--------', len(a[80]))
    # print('a', a)
    # print('b', b)


# need freq to midi note equation


def test_fft_freq():
    freqs = fft_frequencies(sr=22050, n_fft=2048 * 2)
    print('----------- freqs')
    print('len', len(freqs))
    print(freqs)
    print('-----------')
    # midis = [hz_to_midi(a) for a in freqs]
    midis = hz_to_midi(freqs)
    print('midis len', len(midis))
    fout = open('midi_fft_freqs.txt', 'w')
    for m in midis:
        # fout.writelines
        fout.write('%s\n' % m)
    # print(midis)


if __name__ == '__main__':
    test_fft_freq()
