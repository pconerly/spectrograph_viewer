import librosa
import numpy as np
# from functools import enumerate
from state.thunks import callAndSave

from db import SirensFile, StatusEnum, session


def getMostRecentSirensFile(fp):
    target = session.query(SirensFile).filter_by(filepath=fp).order_by(
        SirensFile.last_updated.desc()).first()
    return target


fp = '/Users/peterconerly/code/sirens/Arcade Fire - City With No Children.mp3'
fp = '/Users/peterconerly/code/sirens/treetop_01_intro.mp3'


def resaveTestFile():
    pass
    callAndSave(fp)


def missingNotes():
    pass

    # derps = session.query(SirensFile).all()
    target = getMostRecentSirensFile(fp)

    if target == None:
        callAndSave(fp)
        target = getMostRecentSirensFile(fp)

    # print(derps)

    # target = derps[0]

    print(target)
    print("----")
    supporting_data = target.getData()
    print("supporting_data", supporting_data.keys())

    n_mels = supporting_data['n_mels']
    f_mels = supporting_data['f_mels']
    print('---- n_mels', n_mels)
    print('---- f_mels')
    midi_f = np.vectorize(
        librosa.hz_to_midi
    )  # or use a different name if you want to keep the original f
    midi_mels = midi_f(f_mels)
    present_notes = []
    missing_notes = []
    for i, item in enumerate(f_mels):
        midi_note = midi_mels[i]
        print('    %.2f -- %.2f' % (midi_note, item))
        # if (i >= 21 and i <= 108):
        present_notes.append(round(midi_note))

    print('present_notes', len(present_notes))
    for i in range(21, 109):
        if not i in present_notes:
            missing_notes.append(i)

    # specto = target.getSpectograph()
    # print('specto', specto)
    # for d in dir(target.spectograph):
    #     print(d)
    # print('python_type', target.spectograph.python_type)
    # print('length', target.spectograph.length)

    # res = target.spectograph.copy_value()
    print("----")

    print('missing_notes len:', len(missing_notes))
    for mn in missing_notes:
        print('  ', mn)
    # print("res", res)
    # print('len', len(res))
    print("----")


if __name__ == '__main__':
    # missingNotes()

    resaveTestFile()