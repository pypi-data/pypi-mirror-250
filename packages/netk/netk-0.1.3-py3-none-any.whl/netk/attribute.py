class NAttribute(object):
    def __init__(self, obj, name: str, split: str = "_"):
        self.obj = obj
        self.name = name

        self.name_attr = self.name
        self.name_set = "set" + split + self.name  # self.set_{name}
        self.name_get = "get" + split + self.name  # self.get_{name}
        self.name_del = "del" + split + self.name  # self.get_{name}
        self.name_setget = self.name

        def set(__value):
            setattr(self.obj, self.name_attr, __value)

        def get():
            return getattr(self.obj, self.name_attr)

        def del0():
            delattr(self.obj, self.name_attr)

        attr = property(get, set, del0)

        setattr(self.obj, self.name_set, set)  # 动态添加设置属性方法
        setattr(self.obj, self.name_get, get)  # 动态添加获取属性方法
        setattr(self.obj, self.name_del, del0)  # 动态添加删除属性方法
        setattr(self.obj, self.name_setget, attr)


class NAttributeWarp(object):
    def __init__(self, obj, name: str, split: str = "_"):
        self.obj = obj
        self.obj2 = obj._
        self.name = name

        self.name_attr = self.name
        self.name_set = "set" + split + self.name  # self.set_{name}
        self.name_get = "get" + split + self.name  # self.get_{name}
        self.name_del = "del" + split + self.name  # self.get_{name}
        self.name_setget = self.name

        def set(__value):
            setattr(self.obj2, self.name_attr, __value)

        def get():
            return getattr(self.obj2, self.name_attr)

        def del0():
            delattr(self.obj2, self.name_attr)

        attr = property(get, set, del0)

        setattr(self.obj, self.name_set, set)  # 动态添加设置属性方法
        setattr(self.obj, self.name_get, get)  # 动态添加获取属性方法
        setattr(self.obj, self.name_del, del0)  # 动态添加删除属性方法
        setattr(self.obj, self.name_setget, attr)