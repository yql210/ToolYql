from collections import Counter
import numpy as np
from mindspore._checkparam import Validator as validator
from .metric import Metric


class BleuScore(Metric):

    def __init__(self, n_gram=4, smooth=False):
        super().__init__()
        # validator.check_value_type为参数的校验
        self.n_gram = validator.check_value_type("n_gram", n_gram, [int])
        if self.n_gram > 4 or self.n_gram < 1:
            raise ValueError('The n_gram value ranged from 1 to 4, but got {}'.format(n_gram))

        self.smooth = validator.check_value_type("smooth", smooth, [bool])
        self.clear()

    def clear(self):
        """清除历史数据"""
        self._numerator = np.zeros(self.n_gram)
        self._denominator = np.zeros(self.n_gram)
        self._precision_scores = np.zeros(self.n_gram)
        self._c = 0.0
        self._r = 0.0
        self._trans_len = 0
        self._ref_len = 0
        self._is_update = False

    # 用ngram计算每个单词在给定文本中出现的次数。
    def _count_ngram(self, ngram_input_list, n_gram):
        # 先构造一个计数器。
        ngram_counter = Counter()

        for i in range(1, n_gram + 1):
            # 遍历翻译文本或参考文本的列表。
            for j in range(len(ngram_input_list) - i + 1):
                # 构造ngram-key字典
                ngram_key = tuple(ngram_input_list[j:(i + j)])
                ngram_counter[ngram_key] += 1

        return ngram_counter

    def update(self, *inputs):
        # 先进行输入个数的判断
        if len(inputs) != 2:
            raise ValueError('The bleu_score need 2 inputs (candidate_corpus, reference_corpus), '
                             'but got {}'.format(len(inputs)))
        # 更新输入，一个为候选句子，一个为参考句子或参考列表
        candidate_corpus = inputs[0]
        reference_corpus = inputs[1]
        # 进行输入的校验
        if len(candidate_corpus) != len(reference_corpus):
            raise ValueError('translate_corpus and reference_corpus should be equal in length, '
                             'but got {} {}'.format(len(candidate_corpus), len(reference_corpus)))
        # 遍历两个输入的每一个单词，使用计数器进行统计
        for (candidate, references) in zip(candidate_corpus, reference_corpus):
            self._c += len(candidate)
            ref_len_list = [len(ref) for ref in references]
            ref_len_diff = [abs(len(candidate) - x) for x in ref_len_list]
            self._r += ref_len_list[ref_len_diff.index(min(ref_len_diff))]
            translation_counter = self._count_ngram(candidate, self.n_gram)
            reference_counter = Counter()

            for ref in references:
                reference_counter |= self._count_ngram(ref, self.n_gram)

            ngram_counter_clip = translation_counter & reference_counter

            for counter_clip in ngram_counter_clip:
                self._numerator[len(counter_clip) - 1] += ngram_counter_clip[counter_clip]

            for counter in translation_counter:
                self._denominator[len(counter) - 1] += translation_counter[counter]

        self._trans_len = np.array(self._c)
        self._ref_len = np.array(self._r)
        self._is_update = True

    def eval(self):
        # 如果_is_update是False，则说明使用方法错误。
        if self._is_update is False:
            raise RuntimeError('Call the update method before calling eval.')

        # 分母不能为0
        if min(self._numerator) == 0.0:
            return np.array(0.0)

        # 计算准确度
        if self.smooth:
            precision_scores = np.add(self._numerator, np.ones(self.n_gram)) / np.add(self._denominator,
                                                                                      np.ones(self.n_gram))
        else:
            precision_scores = self._numerator / self._denominator

        # 使用公式进行计算BLEU
        log_precision_scores = np.array([1.0 / self.n_gram] * self.n_gram) * np.log(precision_scores)
        # 几何平均形式求平均值然后加权
        geometric_mean = np.exp(np.sum(log_precision_scores))
        brevity_penalty = np.array(1.0) if self._c > self._r else np.exp(1 - (self._ref_len / self._trans_len))
        bleu = brevity_penalty * geometric_mean

        return bleu