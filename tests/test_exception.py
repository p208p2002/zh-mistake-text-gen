from zh_mistake_text_gen.data_maker import *
from zh_mistake_text_gen.exception import *

def test_MistakeTextHappendOnDisableWordsError():
    maker = MistakWordMaker()
    try:
        maker("的")
    except MistakeTextHappendOnDisableWordsError:
        assert True
        return
    assert False