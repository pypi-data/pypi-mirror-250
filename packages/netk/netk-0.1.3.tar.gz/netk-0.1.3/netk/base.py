from .attribute import NAttribute
from .object import NObject


class NBase(NObject):

    _type = None

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._ = self._type(*args, **kwargs)

    def bind(self, name, func):
        _ = getattr(self._, name)
        _ += func

    def unbind(self, name, func):
        _ = getattr(self._, name)
        _ -= func