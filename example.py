from zh_mistake_text_aug import Pipeline
import random

random.seed(7)
pipeline = Pipeline()
augs = pipeline("中文語料生成")
for aug in augs:
    print(aug)