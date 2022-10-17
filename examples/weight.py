import sys
sys.path.append('./')
sys.path.append('../')
from zh_mistake_text_gen.data_maker import *
from zh_mistake_text_gen import Pipeline
import random
random.seed(0)
if __name__ =="__main__":
    pipeline = Pipeline(
        makers=[PronounceSimilarWordPlusMaker(level=2),MistakeWordHighFreqMaker(),PronounceSameVocabMaker()],
        maker_weight=[0.2,0.2,0.6]
    )

    results = pipeline(
        "維基的基本設計理念是，與其避免人們犯錯，倒不如讓人們更方便地修正錯誤",
        error_per_sent=3,
        no_change_on_gen_fail=True
    )

    print(results.correct)
    print(results.incorrect)