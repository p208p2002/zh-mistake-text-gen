import sys
sys.path.append('./')
sys.path.append('../')

from zh_mistake_text_gen import Pipeline
import random

random.seed(20)
pipeline = Pipeline()
incorrect_sent = pipeline("中文語料生成")
print(incorrect_sent)