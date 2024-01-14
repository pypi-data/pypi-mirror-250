from .attribute import NAttribute


class NObject(object):
    def __init__(self):
        pass

    def create_attr(self, attr_name: str, attr_split: str = "_"):
        attribute = NAttribute(self, attr_name, attr_split)
        attribute_name = "_nattribute_" + attr_name
        setattr(self, attribute_name, attribute)  # self._{attr_name}

    def create_attr_warp(self, attr_name: str, attr_split: str = "_"):
        attribute = NAttribute(self, attr_name, attr_split)
        attribute_name = "_nattribute_warp_" + attr_name
        setattr(self, attribute_name, attribute)  # self._{attr_name}
