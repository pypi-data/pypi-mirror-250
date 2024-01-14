from .object import NObject


class NImport(NObject):
    def __init__(self, libname):
        super().__init__()
        self.libname = libname
        from clr import AddReference
        AddReference(self.libname)