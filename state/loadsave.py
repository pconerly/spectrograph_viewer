import os
from attrdict import AttrDict
import yaml

from utils import getRightDirs

resource_dir, data_path = getRightDirs()

savefile = os.path.join(data_path, 'state.yaml')


def makeSaveObj(state):
    toSave = {
        'filename': state.filename,
        'curDir': state.curDir,
        'showSirensFiles': state.showSirensFiles
    }
    return toSave


def saveState(state):
    toSave = makeSaveObj(state)
    with open(savefile, 'w') as fout:
        fout.write(yaml.dump(toSave, default_flow_style=False))


def loadState():
    if os.path.exists(savefile):
        with open(savefile, 'r') as fin:
            data = fin.read()
            data = yaml.load(data)
            return data
    return {}


if __name__ == '__main__':
    save(AttrDict({'filename': 'derp', 'curDir': 'what'}))

    derp = {
        'name': "The Cloak 'Colluin'",
        'depth': 5,
        'rarity': 45,
        'weight': 10,
        'cost': 50000,
        'flags': ['INT', 'WIS', 'SPEED', 'STEALTH']
    }

    load()
