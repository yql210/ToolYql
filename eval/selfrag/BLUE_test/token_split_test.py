import spacy

# 加载中文模型
nlp = spacy.load("zh_core_web_sm")

# 待分词的文本
text = "乐器，旋律，和声，节奏，节拍，唱片，演出，音符，音乐家，曲调"

# 使用nlp对象处理文本
doc = nlp('乐器，旋律，和声，节奏，节拍，唱片，演出，音符，音乐家，曲调')

# 遍历文档中的词（token）
for token in doc:
    print(token.text, end=' ')

