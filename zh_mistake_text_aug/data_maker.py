import random
from loguru import logger
import jieba
from .utils import Pronounce2Word
from abc import ABC
from opencc import OpenCC
from typing import Any
from .data_model import NoiseCorpus
from .exception import DataNotFundError,FindOrConvertError
import os
import py_chinese_pronounce
from copy import copy

high_freq_zh_char_path = os.path.join(
    os.path.dirname(__file__),
    'high_freq_zh_char.txt'
)

class BaseDataMaker(ABC):
    def __init__(self,*args,**kwargs) -> None:
        self.t2s = OpenCC('t2s.json').convert
        self.setup()

    def setup(self):
        """
        Do something if needed
        """
        pass

    def make(self,x)->NoiseCorpus:
        raise NotImplementedError
    
    def __call__(self, *args: Any, **kwargs: Any)-> NoiseCorpus:
        data = self.make(*args,**kwargs)
        data.type = self.__class__.__name__

        if self.t2s(data.correct) == self.t2s(data.incorrect):
            raise FindOrConvertError('After t2s compare is same')

        return data

class MissingWordMaker(BaseDataMaker):
    def make(self, x)->NoiseCorpus:
        correct = x[:]
        rand = random.randint(0, len(x)-1)
        x = list(x)
        span = x.pop(rand)
        x = ''.join(x)

        return NoiseCorpus(
            correct=correct,
            incorrect=x,
        )

class MissingVocabMaker(BaseDataMaker):
    def make(self,x)->NoiseCorpus:
        correct = x[:]
        seg_list = list(jieba.cut(x))
        rand = random.randint(0, len(seg_list)-1)
        span = seg_list.pop(rand)

        return NoiseCorpus(
            correct=correct,
            incorrect=''.join(seg_list)
        )

class PronounceSimilarWordMaker(BaseDataMaker):
    """
    去除聲符找相似
    """
    def __init__(self,*args,p2w=None,**kwargs):
        super().__init__()
        if p2w is not None:
            self.p2w = p2w
        else:
            self.p2w = Pronounce2Word()

    def make(self,x):
        correct = x[:]
        rand = random.randint(0, len(x)-1)

        replace_word = x[rand]

        try:
            similar_vocab = self.p2w.find_similar(replace_word)
        except:
            raise FindOrConvertError('p2w find similar error')

        rand_for_select_similar_word = random.randint(0, len(similar_vocab)-1)
        select_similar_word = similar_vocab[rand_for_select_similar_word]

        x = [c for c in x]
        x[rand] = select_similar_word
        x = ''.join(x)

        return NoiseCorpus(
            correct=correct,
            incorrect=x
        )

class PronounceSimilarWordPlusMaker(BaseDataMaker):
    """
    編輯距離找相似+高頻字
    """
    def __init__(self,*args,p2w=None,level=1,**kwargs):
        super().__init__()
        self.level = level
        if p2w is not None:
            self.p2w = p2w
        else:
            self.p2w = Pronounce2Word()
    
    def setup(self):
        self.high_freq_zh_char = []
        f = open(high_freq_zh_char_path, encoding='utf-8')
        for line in f.readlines():
            self.high_freq_zh_char.append(line.replace('\n', ''))
        f.close()


    def make(self,x):
        correct = x[:]
        rand = random.randint(0, len(x)-1)

        replace_word = x[rand]

        try:
            new_han_pronounces = self.p2w._find_similar_han_pronounces(self.p2w.to_han(replace_word),level=self.level)
        except:
            raise FindOrConvertError

        random.shuffle(new_han_pronounces)
        new_han_pronounce = new_han_pronounces[0]
        new_words = self.p2w.han2word(new_han_pronounce)
        new_words = list(filter(lambda x:x in self.high_freq_zh_char,new_words))

        if len(new_words) == 0:
            raise DataNotFundError("No high freq char in string")

        random.shuffle(new_words)
        new_word = new_words[0]

        if new_word == replace_word:
            raise DataNotFundError("same word")
        
        rand_for_select_similar_word = random.randint(0, len(new_word)-1)
        select_similar_word = new_word[rand_for_select_similar_word]

        x = [c for c in x]
        x[rand] = select_similar_word
        x = ''.join(x)

        return NoiseCorpus(
            correct=correct,
            incorrect=x
        )

class PronounceSameWordMaker(BaseDataMaker):
    def __init__(self,*args,p2w=None,**kwargs):
        super().__init__()
        if p2w is not None:
            self.p2w = p2w
        else:
            self.p2w = Pronounce2Word()
            
    def make(self,x):
        correct = x[:]
        rand = random.randint(0, len(x)-1)

        replace_word = x[rand]

        try:
            similar_vocab = self.p2w.find_same(replace_word)
        except:
            raise FindOrConvertError

        if len(similar_vocab) == 0:
            raise DataNotFundError('similar_vocab not found')

        rand_for_select_similar_word = random.randint(0, len(similar_vocab)-1)
        select_similar_word = similar_vocab[rand_for_select_similar_word]

        x = [c for c in x]
        x[rand] = select_similar_word
        x = ''.join(x)

        return NoiseCorpus(
            correct=correct,
            incorrect=x
        )


class PronounceSimilarVocabMaker(BaseDataMaker):
    def __init__(self,*args,p2w=None,**kwargs):
        super().__init__()
        if p2w is not None:
            self.p2w = p2w
        else:
            self.p2w = Pronounce2Word()

    def make(self,x):
        correct = x[:]
        seg_list = list(jieba.cut(x))
        rand = random.randint(0, len(seg_list)-1)
        span = seg_list[:].pop(rand)

        try:
            similar_pronounce_spans = self.p2w.find_similar_vocab(span)
        except:
            raise FindOrConvertError
        if len(similar_pronounce_spans) == 0:
            raise DataNotFundError('similar_pronounce_spans not found')
        random.shuffle(similar_pronounce_spans)
        similar_pronounce_span = similar_pronounce_spans[0]

        seg_list[rand] = similar_pronounce_span
        x = seg_list
        x = ''.join(x)

        return NoiseCorpus(
            correct=correct,
            incorrect=x
        )

class PronounceSameVocabMaker(BaseDataMaker):
    def __init__(self,*args,p2w=None,**kwargs):
        super().__init__()
        if p2w is not None:
            self.p2w = p2w
        else:
            self.p2w = Pronounce2Word()

    def make(self,x):
        correct = x[:]
        seg_list = list(jieba.cut(x))
        rand = random.randint(0, len(seg_list)-1)
        span = seg_list[:].pop(rand)

        try:
            similar_pronounce_spans = self.p2w.find_same_vocab(span)
        except:
            raise FindOrConvertError

        if len(similar_pronounce_spans) == 0:
            raise DataNotFundError('similar_pronounce_spans not found')
        random.shuffle(similar_pronounce_spans)
        similar_pronounce_span = similar_pronounce_spans[0]

        # logger.debug(f"{rand} {seg_list}")
        seg_list[rand] = similar_pronounce_span
        x = seg_list
        x = ''.join(x)

        return NoiseCorpus(
            correct=correct,
            incorrect=x
        )

class RedundantWordMaker(BaseDataMaker):
    def __init__(self,*args,p2w=None,**kwargs):
        super().__init__()
        if p2w is not None:
            self.p2w = p2w
        else:
            self.p2w = Pronounce2Word()
            
    def make(self,x):
        correct = x[:]
        rand = random.randint(0, len(x)-1)
        x = list(x)
        span = x[rand-1]
        x.insert(rand, x[rand-1])
        x = ''.join(x)
        return NoiseCorpus(
            correct=correct,
            incorrect=x
        )

class MistakWordMaker(BaseDataMaker):
    def __init__(self,*args,p2w=None,**kwargs):
        super().__init__()
        if p2w is not None:
            self.p2w = p2w
        else:
            self.p2w = Pronounce2Word()
    def make(self,x):
        ch_unis = list(self.p2w.uni2cns_map.keys())
        random_ch_uni_index = random.randint(0, len(ch_unis))

        try:
            random_ch = self.p2w._uni2word(ch_unis[random_ch_uni_index])
        except:
            raise FindOrConvertError("p2w._uni2word out of range")

        correct = x[:]
        rand = random.randint(0, len(x)-1)
        span = random_ch

        x = list(x)
        x[rand] = span
        x = ''.join(x)

        return NoiseCorpus(
            correct=correct,
            incorrect=x
        )

class MistakeWordHighFreqMaker(BaseDataMaker):
    def setup(self):
        self.high_freq_zh_char = []
        f = open(high_freq_zh_char_path, encoding='utf-8')
        for line in f.readlines():
            self.high_freq_zh_char.append(line.replace('\n', ''))
        f.close()

    def make(self,x):
        random_ch_uni_index = random.randint(0, len(self.high_freq_zh_char)-1)
        random_ch = self.high_freq_zh_char[random_ch_uni_index]

        correct = x[:]
        rand = random.randint(0, len(x)-1)
        span = random_ch

        x = list(x)
        x[rand] = span
        x = ''.join(x)

        return NoiseCorpus(
            correct=correct,
            incorrect=x
        )

class MissingWordHighFreqMaker(BaseDataMaker):
    def setup(self):
        self.high_freq_zh_char = []
        f = open(high_freq_zh_char_path, encoding='utf-8')
        for line in f.readlines():
            self.high_freq_zh_char.append(line.replace('\n', ''))
        f.close()

    def make(self,x):
        high_freq_char_list = []
        for char_x in list(x):
            if char_x in self.high_freq_zh_char:
                high_freq_char_list.append(char_x)

        if len(high_freq_char_list) == 0:
            raise DataNotFundError("No high freq char in string")

        random_ch = random.choice(high_freq_char_list)

        correct = x[:]
        x = list(x)

        rand = x.index(random_ch)
        span = x.pop(rand)
        x = ''.join(x)

        return NoiseCorpus(
            correct=correct,
            incorrect=x
        )

class RandomInsertVacabMaker(BaseDataMaker):
    def setup(self):
        sc_dict_path = os.path.join(
            os.path.dirname(py_chinese_pronounce.__file__),
            'sc-dict.txt'
        )
        self.sc_dict = open(sc_dict_path,'r').read().split()

    def make(self,x):
        correct = x[:]
        x = x[:]
        random_vocab = self.sc_dict[random.randint(0,len(self.sc_dict)-1)]
        rand_ins_postion = random.randint(0,len(x))
        x = list(x)
        x.insert(rand_ins_postion,random_vocab)
        x = ''.join(x)

        return NoiseCorpus(
            correct=correct,
            incorrect=x
        )

class Pipeline():
    def __init__(self,makers=None):
        self.makers = makers
        if makers is None:
            self.makers = []
            for g_var_name in copy(globals()):
                try:
                    if g_var_name != BaseDataMaker.__name__ and issubclass(globals()[g_var_name],BaseDataMaker):
                        print("O",g_var_name)
                        self.makers.append(globals()[g_var_name]())
                except:
                    print("X",g_var_name)
        
    
    def __call__(self,x, verbose=True):        
        out = []
        for maker in self.makers:
            try:
                res = maker(x)
                out.append(res)
            except DataNotFundError:
                """
                it's ok for this error
                """
                pass
            except FindOrConvertError:
                """
                it's ok for this error
                """
                pass
            except Exception as e:
                if verbose:
                    logger.warning(f"{x} - {e} - {maker}")
                exit(1)
        return out
    