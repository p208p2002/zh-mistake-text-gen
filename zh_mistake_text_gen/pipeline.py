from .data_maker import *
from .exception import *
from copy import copy
from loguru import logger

class Pipeline():
    def __init__(self, makers=None, maker_weight=None):
        """
        管道類用於快速呼叫多個`data_maker`方法

        :param makers: Optional 自訂傳入多個`DataMaker`實例
        :param maker_weight: Optional 為每一個 `DataMaker` 設定被選中機率
        """

        self.maker_weight = maker_weight
        self.makers = makers

        if makers is None:
            self.makers = []
            for g_var_name in copy(globals()):
                try:
                    if g_var_name not in [NoChangeMaker.__name__, BaseDataMaker.__name__] and issubclass(globals()[g_var_name], BaseDataMaker):
                        print("O", g_var_name)
                        self.makers.append(globals()[g_var_name]())
                    else:
                        print("X", g_var_name)
                except:
                    print("X", g_var_name)

        if self.maker_weight != None:
            assert len(self.maker_weight) == len(
                self.makers), 'While have `maker_weight` must provide maker_weight for each maker'

    def _noraml_call(self, x, k, no_change_on_gen_fail=False, verbose=True, makers=None):
        out = []

        if makers is None:
            makers = self.makers

        for maker in makers:
            retry = 0
            while retry < 5:
                try:
                    res = maker(x)
                    out.append(res)
                    break
                except Exception as e:
                    retry += 1
                    if verbose:
                        logger.warning(
                            f"{x} - {e} - {type(e)} - {maker} retry:{retry}")


        if len(out) == 0 and not no_change_on_gen_fail:
            raise  ZeorSearchResultsError("Data gen fail, len(out) == 0")
        elif len(out) == 0 and no_change_on_gen_fail:
            return [NoiseCorpus(
                correct=x,
                incorrect=x,
                type=NoChangeMaker.__name__
            )]

        random.shuffle(out)
        return out[:k]

    def _weight_call(self, x, k, no_change_on_gen_fail, verbose=True):
        makers = random.choices(
            population=self.makers,
            weights=self.maker_weight,
            k=k
        )

        return self._noraml_call(x, k, no_change_on_gen_fail, verbose, makers)

    def __call__(self, x, error_per_sent=1, no_change_on_gen_fail=False, verbose=True):
        """
        呼叫管道生成資料

        :param x: 一段正確的中文句子
        :param error_per_sent: Optional 在句子中生成多少錯誤
        :param no_change_on_gen_fail: 當生成失敗的時候允許使用原句（即不變換），啟用時不拋出錯誤，反之。預設:`False`
        :param verbose: 除錯或額外訊息
        :type x: str
        :type error_pre_sent: int
        :type no_change_on_gen_fail: bool
        :type verbose: bool
        :retrun: 包含錯誤句子的物件
        """

        ori_x = x
        assert error_per_sent >= 1
        error_types = []
        for i in range(error_per_sent):
            if self.maker_weight is None:
                out = self._noraml_call(x, 1, no_change_on_gen_fail, verbose)
                x = out[0].incorrect
            else:
                out = self._weight_call(x, 1, no_change_on_gen_fail, verbose)
                x = out[0].incorrect
            
            #
            error_types.append(out[0].type)

        for o in out: 
            o.correct = ori_x
        
        out[0].type = '_'.join(error_types)
        return out[0]