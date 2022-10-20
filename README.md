# 錯誤類型中文語料生成
## 安裝
```bash
pip install zh-mistake-text-gen
```
## 使用 (Pipeline)
```python
from zh_mistake_text_gen import Pipeline
pipeline = Pipeline()
incorrect_sent = pipeline("中文語料生成")
print(incorrect_sent)
# type='PronounceSimilarVocabMaker' correct='中文語料生成' incorrect='鍾文語料生成' incorrect_start_at=0 incorrect_end_at=2 span='鍾文'
```
## 文檔
### `Pipeline`
- `__init__`
    - `makers` = None : maker實例，可選
    - `maker_weight` = None : maker被抽中的機率，可選

- `__call__`
    - `x` : 輸入句(str)，必需
    - `error_per_sent`: 每句要多少錯誤。預設:`1`
    - `no_change_on_gen_fail`: 生成方法失敗的時候允許不變動。啟用時不拋出錯誤，反之。預設:`False`
    - `verbose`=True : debug 訊息，可選

## 可用方法
```python
from zh_mistake_text_gen.data_maker import *
```
|Data Maker|Description|
|---|---|
|NoChangeMaker|沒有任何變換|
|MissingWordMaker|隨機缺字|
|MissingVocabMaker|隨機缺詞|
|PronounceSimilarWordMaker|隨機相似字替換|
|PronounceSimilarWordPlusMaker|編輯距離找發音相似並且用高頻字替換|
|PronounceSimilarVocabMaker|發音相似詞替換|
|PronounceSimilarVocabPlusMaker|編輯距離找發音相似發音相似詞替換|
|PronounceSameWordMaker|發音相同字替換|
|PronounceSameVocabMaker|發音相同詞替換|
|RedundantWordMaker|隨機複製旁邊一個字作為沆於字|
|RandomInsertVacabMaker|隨機插入詞彙|
|MistakWordMaker|隨機替換字|
|MistakeWordHighFreqMaker|隨機替換高頻字|
|MissingWordHighFreqMaker|隨機刪除高頻字|