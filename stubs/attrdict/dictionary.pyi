from attrdict.mixins import MutableAttr

class AttrDict(dict, MutableAttr):
    def __init__(self, *args, **kwargs) -> None: ...
