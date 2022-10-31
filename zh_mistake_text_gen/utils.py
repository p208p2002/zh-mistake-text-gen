from py_chinese_pronounce import Pronounce2Word as _Pronounce2Word
import os
import edit_distance

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

disable_words = open(
    os.path.join(
        os.path.dirname(__file__),
        "disable_words.txt"
    ),
    "r",encoding="utf-8"
).read().split()

def is_mistake_happend_on_disable_words(ori_snet,new_snet):
    sm = edit_distance.SequenceMatcher(a=ori_snet, b=new_snet)
    for op_code in sm.get_opcodes():
        operation_name,a_start,a_end,b_start,b_end = op_code
        if operation_name != "equal":
            a_span = ori_snet[a_start:a_end]
            b_span = new_snet[b_start:b_end]
            if a_span in disable_words or b_span in disable_words:
                return True
    return False