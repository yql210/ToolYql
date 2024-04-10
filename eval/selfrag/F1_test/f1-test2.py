from sklearn.metrics import classification_report

# 结果评估
# 假设y_true是真实的标签，y_pred是预测的标签
y_true = [0, 1, 3, 2, 3, 0, 2, 2, 3, 3, 3, 0, 1, 4, 4, 0, 1, 3, 2, 2, 1, 3, 2, 0, 2, 4, 1, 0, 1, 0, 4, 3, 3, 3, 2, 1, 0, 3, 0]
y_pred = [0, 1, 3, 0, 2, 0, 2, 2, 1, 2, 3, 0, 0, 4, 4, 0, 1, 4, 2, 2, 0, 3, 2, 1, 2, 4, 3, 1, 1, 3, 4, 3, 0, 2, 2, 3, 2, 2, 1]

print(classification_report(y_true, y_pred, target_names=['C1','C2','C3','C4','C5']))

