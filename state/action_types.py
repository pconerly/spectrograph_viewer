from attrdict import AttrDict

actionTypesList = [
    'changeFocus',
    'toggleFilePicking',
    'filePickingFired',
    'updateTmpDir',
    'changeTmpDir',
    'loadFile',
    'filePicked',
    'closePopup',
    'clearClosePopup',
    'playPauseAudio',
    'stopAudio',
    'setSpectoPosition',
    'closeFileViewer',
    'setLocalStartTime',
    'setShowSirensFiles',
    'sirenfilePopupFires',
    'sirenfilePopupFired',
    'sirenfilePopupClose',
    'deleteSirenfile',
    'showTestWindow',
]

actionTypes = AttrDict({k: k for k in actionTypesList})
