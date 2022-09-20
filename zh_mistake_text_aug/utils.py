from py_chinese_pronounce import Pronounce2Word as _Pronounce2Word

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class Pronounce2Word(_Pronounce2Word):
    pass