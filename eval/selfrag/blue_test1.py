from nltk.translate.bleu_score import sentence_bleu, corpus_bleu
from nltk.translate.bleu_score import SmoothingFunction

reference = [['The', 'cat', 'is', 'on', 'the', 'mat']]
candidate = ['The', 'cat', 'sat', 'on', 'the', 'mat']
smooth = SmoothingFunction()  # 定义平滑函数对象
score = sentence_bleu(reference, candidate, weights=(0.25,0.25, 0.25, 0.25), smoothing_function=smooth.method1)
corpus_score = corpus_bleu([reference], [candidate], smoothing_function=smooth.method1)

print('end')