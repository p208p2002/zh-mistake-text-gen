import sys
sys.path.append('./')
sys.path.append('../')

from zh_mistake_text_gen import Pipeline
import random

random.seed(7)
pipeline = Pipeline()
augs = pipeline("中文語料生成",k=3)
for aug in augs:
    print(aug)