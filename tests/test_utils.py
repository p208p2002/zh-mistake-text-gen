from zh_mistake_text_gen.utils import *

def test_is_mistake_happend_on_disable_words():
    ori_a = "下雨的聲音"
    new_b = "下雨地聲音"
    assert is_mistake_happend_on_disable_words(ori_a,new_b) == True

    ori_a = "下雨的聲音"
    new_b = "下與的聲音"
    assert is_mistake_happend_on_disable_words(ori_a,new_b) == False
    
    ori_a = "下雨的聲音"
    new_b = "下雨聲音"
    assert is_mistake_happend_on_disable_words(ori_a,new_b) == True

    ori_a = "下雨的聲音"
    new_b = "下雨的聲音嗎"
    assert is_mistake_happend_on_disable_words(ori_a,new_b) == True

    ori_a = "下雨的聲音"
    new_b = "聽見下雨的聲音"
    assert is_mistake_happend_on_disable_words(ori_a,new_b) == False

    ori_a = "黃先生你好"
    new_b = "陳先生你好"
    assert is_mistake_happend_on_disable_words(ori_a,new_b) == True

    ori_a = "黃先生你好"
    new_b = "黃先生妳好"
    assert is_mistake_happend_on_disable_words(ori_a,new_b) == True

    ori_a = "黃生生你好"
    new_b = "黃先聲你好"
    assert is_mistake_happend_on_disable_words(ori_a,new_b) == False

    ori_a = "黃生生你好"
    new_b = "黃先聲你好嗎"
    assert is_mistake_happend_on_disable_words(ori_a,new_b) == True
