class ZeorSearchResultsError(Exception):
    """
    搜尋替換時沒有可用的選項或結果
    """
    pass

class TraditionalSimplifiedSameError(Exception):
    """
    簡繁轉換後相同
    """
    pass

class FindOrConvertError(Exception):
    """
    尋找資料或是轉換時發生錯誤
    """
    pass

class MistakeTextHappendOnDisableWordsError(Exception):
    """
    產生錯誤文字發生在禁用字上
    """