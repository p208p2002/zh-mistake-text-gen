from zh_mistake_text_gen import Pipeline
import time
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
    makers = pipeline.makers
    all_maker_type = [maker.__class__.__name__ for maker in makers]
    print(all_maker_type)
    time.sleep(3)


    already_gen_type = set()
    for i in range(2000):
        for test_input in test_inputs:
            results = pipeline(test_input,verbose=False)
            
            if results.type not in already_gen_type:
                print(results.type)
                print(results.correct)
                print(results.incorrect)                
                already_gen_type.update([results.type])
                time.sleep(1)
        
        if len(already_gen_type) == len(all_maker_type):
            break
        else:
            print("unused maker:",list(filter(lambda maker_type: maker_type not in already_gen_type,all_maker_type)))
            time.sleep(1)
        
    if len(already_gen_type) != len(all_maker_type):
        assert False
