import sys
sys.path.append('./')
sys.path.append('../')

from zh_mistake_text_gen import Pipeline
from zh_mistake_text_gen.data_maker import *
import random


def get_pipeline():
    """
    將個生產器用群組分類，然後給定群組機率
    回傳一個實例過後的pipeline(包含機率分佈)
    """
    group_del = [MissingWordMaker,MissingVocabMaker,MissingWordHighFreqMaker]

    group_ins = [RedundantWordMaker,RandomInsertVacabMaker]

    group_rep = [
        PronounceSimilarWordMaker,
        PronounceSimilarWordPlusMaker,
        PronounceSimilarVocabMaker,
        PronounceSameWordMaker,
        PronounceSameVocabMaker,
        MistakWordMaker,
        MistakeWordHighFreqMaker
    ]

    group_weights = [
        0.02,
        0.14,
        0.84
    ]

    makers = []
    maker_weights = []

    for group_weight,group_makers in zip(group_weights,[group_del,group_ins,group_rep]):
        for m in group_makers:
            makers.append(m()) # instance class
            maker_weights.append(group_weight/len(group_makers))
    
    for w,m in zip(maker_weights,makers):
        print(w,m)

    p = Pipeline(
        makers=makers,
        maker_weight=maker_weights
    )

    return p

if __name__ =="__main__":
    random.seed(0)
    pipeline = get_pipeline()

    results = pipeline(
        "維基的基本設計理念是，與其避免人們犯錯，倒不如讓人們更方便地修正錯誤",
        error_per_sent=3,
        no_change_on_gen_fail=True
    )

    print(results.correct)
    print(results.incorrect)