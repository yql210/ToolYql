from nltk.translate.bleu_score import sentence_bleu, corpus_bleu

# # 示例参考翻译和机器翻译输出
# references = [['The', 'cat', 'is', 'on', 'the', 'mat']]
# candidates = [['The', 'cat', 'sat', 'on', 'the', 'mat']]
#
# # 计算单个句子的BLEU分数
# sentence_bleu_score = sentence_bleu(references, candidates)
# print(f"Sentence BLEU Score: {sentence_bleu_score}")
#
# # 示例多个参考翻译和多个机器翻译输出
# references_corpus = [
#     ['The', 'cat', 'is', 'on', 'the', 'mat'],
#     ['There', 'is', 'a', 'cat', 'on', 'the', 'mat']
# ]
# candidates_corpus = [
#     ['The', 'cat', 'sat', 'on', 'the', 'mat'],
#     ['The', 'cat', 'is', 'on', 'the', 'mat']
# ]
#
# # 计算整个语料库的BLEU分数
# corpus_bleu_score = corpus_bleu(references_corpus, candidates_corpus)
# print(f"Corpus BLEU Score: {corpus_bleu_score}")


# 假设我们有一些机器翻译的句子（机器翻译输出）和参考翻译的句子
# 这里我们用单个句子和参考翻译作为示例
machine_translation = "The home is wonderful"
references = ["The house is amazing", "The home is wonderful"]

# 计算 BLEU 分数
bleu_score = sentence_bleu([references], machine_translation)

# 打印 BLEU 分数
print(f"BLEU Score: {bleu_score:.4f}")