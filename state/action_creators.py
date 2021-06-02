from attrdict import AttrDict
from .action_types import actionTypes


def openFilepicker():
    return {
        'type': actionTypes.toggleFilePicking,
        'payload': True,
    }


def close_filepicker():
    return {
        'type': actionTypes.toggleFilePicking,
        'payload': False,
    }


def filePickingFired():
    return {
        'type': actionTypes.filePickingFired,
    }


def updateTmpDir(newpath):
    return {
        'type': actionTypes.updateTmpDir,
        'payload': newpath,
    }


def loadFile(filepath):
    return {
        'type': actionTypes.loadFile,
        'payload': filepath,
    }


def closePopup():
    return {
        'type': actionTypes.closePopup,
    }


def clearClosePopup():
    return {
        'type': actionTypes.clearClosePopup,
    }


def playPauseAudio():
    return {
        'type': actionTypes.playPauseAudio,
    }


def stopAudio():
    return {
        'type': actionTypes.stopAudio,
    }


def setSpectoPosition(position):
    return {
        'type': actionTypes.setSpectoPosition,
        'payload': {
            'position': position
        }
    }


def setLocalStartTime(position):
    return {
        'type': actionTypes.setLocalStartTime,
        'payload': {
            'position': position
        }
    }


def closeFileViewer():
    return {
        'type': actionTypes.closeFileViewer,
    }


def setShowSirensFiles(showing):
    return {
        'type': actionTypes.setShowSirensFiles,
        'payload': showing,
    }


def sirenfilePopupFires(index):
    return {'type': actionTypes.sirenfilePopupFires, 'payload': index}


def sirenfilePopupFired():
    return {'type': actionTypes.sirenfilePopupFired}


def deleteSirenfile(deleteId):
    return {'type': actionTypes.deleteSirenfile, 'payload': deleteId}


def showTestWindow(showing):
    return {'type': actionTypes.showTestWindow, 'payload': showing}


actions = AttrDict({
    'openFilepicker': openFilepicker,
    'close_filepicker': close_filepicker,
    'filePickingFired': filePickingFired,
    'updateTmpDir': updateTmpDir,
    'loadFile': loadFile,
    'closePopup': closePopup,
    'clearClosePopup': clearClosePopup,
    'playPauseAudio': playPauseAudio,
    'stopAudio': stopAudio,
    'setSpectoPosition': setSpectoPosition,
    'closeFileViewer': closeFileViewer,
    'setLocalStartTime': setLocalStartTime,
    'setShowSirensFiles': setShowSirensFiles,
    'sirenfilePopupFires': sirenfilePopupFires,
    'sirenfilePopupFired': sirenfilePopupFired,
    'deleteSirenfile': deleteSirenfile,
    'showTestWindow': showTestWindow,
})
