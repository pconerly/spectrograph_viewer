import json
from attrdict import AttrDict

from .action_types import actionTypes
from .action_creators import actions

from db import SirensFile, StatusEnum, session

from analysis.run import gen_spectrograph_and_save


def callAndSave(filepath):
    # saves to database
    # returns values to put into state
    sf = SirensFile(filepath)

    log_S, data = gen_spectrograph_and_save(filepath)

    sf.spectograph = log_S.tobytes()
    sf.data = bytearray(json.dumps(data), "utf-8")
    sf.status = StatusEnum.done

    session.add(sf)
    session.commit()

    return log_S, data


def loadFile(dispatch, action):
    filepath = action['payload']
    dispatch(actions.loadFile(filepath))


thunks = AttrDict({'loadFile': loadFile})
