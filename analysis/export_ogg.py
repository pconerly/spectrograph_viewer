import numpy as np

import soundfile as sf


def export_ogg(base_audio_array, filename, sr=44100):
    print('what is sr?: %s' % sr)

    if filename[:4] != ".ogg":
        filename += ".ogg"

    print('start writing')
    print('Writing file: %s' % filename)
    sf.write(filename, base_audio_array, sr)

    print('done writing')
