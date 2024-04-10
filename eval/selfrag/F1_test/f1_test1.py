from sklearn.metrics import classification_report

# 假设y_true是真实的标签，y_pred是预测的标签
y_true = [0, 1, 2, 2, 1]
y_pred = [0, 0, 2, 2, 1]

# 计算F1分数
f1 = f1_score(y_true, y_pred, average='binary')

print("F1分数:", f1)