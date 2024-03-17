
from nltk.translate.bleu_score import sentence_bleu

# 假设我们有一些机器翻译的句子（机器翻译输出）和参考翻译的句子
# 这里我们用单个句子和参考翻译作为示例
machine_translation = "The house is wonderful"
references = ["The house is amazing", "The home is wonderful"]

# 计算 BLEU 分数
bleu_score = sentence_bleu([references], machine_translation)

# 打印 BLEU 分数
print(f"BLEU Score: {bleu_score:.4f}")