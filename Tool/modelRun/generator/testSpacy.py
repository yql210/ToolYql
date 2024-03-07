import spacy

# nlp = spacy.load('en_core_web_sm')
nlp = spacy.load("zh_core_web_sm")


doc = nlp("这是一个用于示例的句子。")
print([(w.text, w.pos_) for w in doc])


