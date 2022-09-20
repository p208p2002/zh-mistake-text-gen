import sys
sys.path.append('./')
sys.path.append('../')

from zh_mistake_text_gen.data_maker import PronounceSimilarWordPlusMaker,MistakeWordHighFreqMaker
from zh_mistake_text_gen import Pipeline

if __name__ =="__main__":
    pipeline = Pipeline(
        makers=[PronounceSimilarWordPlusMaker(level=2),MistakeWordHighFreqMaker()],
        maker_weight=[0.8,0.3]
    )

    results = pipeline(
        "中文語料生成",
        k=10
    )

    for result in results:
        print(result)