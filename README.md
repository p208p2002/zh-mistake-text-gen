# 錯誤類型中文語料生成
## 安裝
```bash
pip install zh-mistake-text-gen
```
## 使用 (Pipeline)
```python
from zh_mistake_text_gen import Pipeline
import random

random.seed(7)
pipeline = Pipeline()
augs = pipeline("中文語料生成",k=8)
for aug in augs:
    print(aug)
```
```
type='MissingWordMaker' correct='中文語料生成' incorrect='中文料生成' incorrect_start_at=2 incorrect_end_at=2 span='語'
type='MissingVocabMaker' correct='中文語料生成' incorrect='語料生成' incorrect_start_at=0 incorrect_end_at=2 span='中文'
type='PronounceSimilarWordMaker' correct='中文語料生成' incorrect='中文語尥生成' incorrect_start_at=3 incorrect_end_at=3 span='尥'
type='PronounceSameWordMaker' correct='中文語料生成' incorrect='諥文語料生成' incorrect_start_at=0 incorrect_end_at=0 span='諥'
type='PronounceSimilarVocabMaker' correct='中文語料生成' incorrect='鍾文語料生成' incorrect_start_at=0 incorrect_end_at=2 span='鍾文'
type='PronounceSameVocabMaker' correct='中文語料生成' incorrect='中文预料生成' incorrect_start_at=2 incorrect_end_at=4 span='预料'
type='RedundantWordMaker' correct='中文語料生成' incorrect='成中文語料生成' incorrect_start_at=0 incorrect_end_at=0 span='成'
type='MistakWordMaker' correct='中文語料生成' incorrect='谁文語料生成' incorrect_start_at=0 incorrect_end_at=0 span='谁'
```

## 文檔
### `Pipeline`
- `__init__`
    - `makers` = None : maker實例，可選
    - `maker_weight` = None : maker被抽中的機率，可選

- `__call__`
    - `x` : 輸入句(str)，必需
    - `k`=1 : 期待最多返回多少結果，可選
    - `verbose`=True : debug 訊息，可選

## 可用方法
```python
from zh_mistake_text_gen.data_maker import *
```
|Data Maker|Description|
|---|---|
|MissingWordMaker|隨機缺字|
|MissingVocabMaker|隨機缺詞|
|PronounceSimilarWordMaker|隨機相似字替換|
|PronounceSimilarWordPlusMaker|編輯距離找發音相似並且用高頻字替換|
|PronounceSimilarVocabMaker|發音相似詞替換|
|PronounceSameWordMaker|發音相同字替換|
|PronounceSameVocabMaker|發音相同詞替換|
|RedundantWordMaker|隨機複製旁邊一個字作為沆於字|
|RandomInsertVacabMaker|隨機插入詞彙|
|MistakWordMaker|隨機替換字|
|MistakeWordHighFreqMaker|隨機替換高頻字|
|MissingWordHighFreqMaker|隨機刪除高頻字|