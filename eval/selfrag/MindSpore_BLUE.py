# import numpy as np
# import mindspore.common.dtype as mstype
# import mindspore.nn as nn
# from mindspore import Tensor

candidate_corpus = [['i', 'have', 'a', 'pen', 'on', 'my', 'desk']]
reference_corpus = [[['i', 'have', 'a', 'pen', 'in', 'my', 'desk'],
                    ['there', 'is', 'a', 'pen', 'on', 'the', 'desk']]]
metric = BleuScore()
metric.clear()
metric.update(candidate_corpus, reference_corpus)
bleu_score = metric.eval()
print(bleu_score)