import sys
sys.path.append('./')
from zh_mistake_text_aug import Pipeline

def test_pipeline():
    test_inputs = [
        ""
        "中文語料生成",
        "英國作家J·K·羅琳的奇幻文學系列小說",
        "磡𧒽犇骉驫",
        "雫",
        "魃魈魁鬾魑魅魍魎",
        "維基媒體基金會是按美國國內稅收法501(c)(3)登記的非營利慈善機構"
    ]
    pipeline = Pipeline()
    for i in range(2000):
        for test_input in test_inputs:
            results = pipeline(test_input,verbose=True)
            for result in results:
                print(i,result)

if __name__ == "__main__":    
    test_pipeline()