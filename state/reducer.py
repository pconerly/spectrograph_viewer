from enum import Enum
import os
import sys
import time

import imgui

from attrdict import AttrDict
import pydux
from .action_types import actionTypes
from .loadsave import loadState, saveState
from .thunks import callAndSave
from db import SirensFile, StatusEnum, session
from audio.queuer import AudioQueuer
from utils import pluck

startDir = os.path.expanduser('~')


class AudioState(Enum):
    Playing = 1
    Stopped = 2


audioPlayer = AudioQueuer()


def read_curdir(state, curDir):
    dirs = list(
        filter(lambda f: os.path.isdir(os.path.join(curDir, f)),
               os.listdir(curDir)))
    files = list(
        filter(lambda f: os.path.isfile(os.path.join(curDir, f)),
               os.listdir(curDir)))
    state.tmpDirs = dirs
    state.tmpFiles = files
    return state


def getMostRecentSirensFile(fp):
    target = session.query(SirensFile).filter_by(filepath=fp).order_by(
        SirensFile.last_updated.desc()).first()
    if target:
        print('-------------- target: %s' % target.last_updated)
    return target


def loadfile(state, process=False):
    filename = state.filename
    if filename:
        sf = getMostRecentSirensFile(filename)
        if sf == None:
            callAndSave(filename)
            sf = getMostRecentSirensFile(filename)

        specto = sf.getSpectograph()
        newfile = AttrDict({
            'spectograph': specto,
            'data': sf.getData(),
        })
        state.file = newfile
        audioPlayer.setup(filename)

    return state


def loadSirensFiles(state):
    if not state.showSirensFiles:
        return state

    targets = session.query(SirensFile).order_by(
        SirensFile.last_updated.desc())

    state.sirenfiles = [
        AttrDict({
            'id': t.id,
            'filepath': t.filepath,
            'filename': os.path.split(t.filepath)[1],
            'status': t.status,
            'last_updated': getattr(t, 'last_updated', None),
        }) for t in targets
    ]

    return state


def deleteSirenFile(state, deleteId):
    session.query(SirensFile).filter_by(id=deleteId).delete()
    session.commit()

    state.sirenfiles = list(
        filter(lambda x: x.id != deleteId, state.sirenfiles))
    return state


def ui_reducer(state, action):
    if state is None:
        ls = loadState()
        newfile = AttrDict({
            'spectograph': None,
            'data': None,
        })
        state = AttrDict({
            'filename': ls.get('filename', None),
            'curDir': ls.get('curDir', startDir),
            'tmpDir': startDir,
            'tmpFiles': [],
            'tmpDirs': [],
            'filePickingFires': False,
            'closePopupFires': False,
            'file': newfile,
            'audioState': AudioState.Stopped,
            'localStartTime': 0,
            'universalStartTime': 0,
            'spectoPos': 0,
            'showSirensFiles': ls.get('showSirensFiles', True),
            'sirenfiles': None,
            # sirens popup
            'sirenPopupFires': False,
            'sirenPopupClose': False,
            'sirenPopupIndex': 0,
            'showTestWindow': False,
        })
        state = loadfile(state)
        state = loadSirensFiles(state)
        state = read_curdir(state, state.tmpDir)

    if action['type'] == actionTypes.toggleFilePicking:
        state.filePickingFires = action['payload']
    elif action['type'] == actionTypes.filePickingFired:
        state.filePickingFires = False

    elif action['type'] == actionTypes.sirenfilePopupFires:
        index = action['payload']
        state.sirenPopupIndex = index
        state.sirenPopupFires = True
    elif action['type'] == actionTypes.sirenfilePopupFired:
        state.sirenPopupFires = False

    elif action['type'] == actionTypes.updateTmpDir:
        state.tmpDir = action['payload']
        state = read_curdir(state, state.tmpDir)

    elif action['type'] == actionTypes.loadFile:
        state.filename = str(action['payload'])
        state = loadfile(state, process=True)
        saveState(state)
        if state.showSirensFiles:
            state = loadSirensFiles(state)

    elif action['type'] == actionTypes.closeFileViewer:
        state.filename = None
        saveState(state)

    elif action['type'] == actionTypes.closePopup:
        state.closePopupFires = True

    elif action['type'] == actionTypes.clearClosePopup:
        state.closePopupFires = False

    elif action['type'] == actionTypes.playPauseAudio:
        if state.audioState == AudioState.Stopped:  # playing
            state.universalStartTime = time.time()
            state.audioState = AudioState.Playing
            audioPlayer.playAudio()

        else:  # pausing
            state.audioState = AudioState.Stopped
            state.localStartTime = state.localStartTime + time.time(
            ) - state.universalStartTime

            (sr, hop_l, x_length) = pluck(state.file.data, 'sr', 'hop_l',
                                          'x_length')
            timeToFrames = (sr / hop_l)

            spectoPosFrame = int(state.spectoPos * timeToFrames)
            drawline = int(state.localStartTime * timeToFrames)
            # state.spectoPos = state.localStartTime

            if drawline + 100 > spectoPosFrame + 680:
                spectoPosFrame = int(drawline + 100 - 680)

            # correct for overzealousness
            spectoPosFrame = min(spectoPosFrame, x_length - 680)
            state.spectoPos = spectoPosFrame / timeToFrames

            audioPlayer.pauseAudio()

    elif action['type'] == actionTypes.stopAudio:
        state.localStartTime = 0
        state.audioState = AudioState.Stopped
        audioPlayer.pauseAudio()
        audioPlayer.rewind()

    elif action['type'] == actionTypes.setSpectoPosition:
        pos = action.get('payload', {}).get('position', 0)
        state.spectoPos = pos

    elif action['type'] == actionTypes.setLocalStartTime:
        pos = action.get('payload', {}).get('position', 0)
        state.localStartTime = pos
        audioPlayer.seekToTime(pos)

    elif action['type'] == actionTypes.setShowSirensFiles:
        showing = action.get('payload', False)
        state.showSirensFiles = showing
        if showing:
            state = loadSirensFiles(state)

        saveState(state)

    elif action['type'] == actionTypes.deleteSirenfile:
        state = deleteSirenFile(state, action['payload'])

    elif action['type'] == actionTypes.showTestWindow:
        state.showTestWindow = action['payload']

    return state


def setup_store():
    store = pydux.create_store(ui_reducer)
    return store
