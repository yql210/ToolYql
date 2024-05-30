import matplotlib.pyplot as plt

# 假设你的数据如下：
metrics = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]  # F1, Hits@1, Acc等指标
training_data_percentages = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # 训练数据的百分比

metrics = [45.1, 49.7, 52.3, 55.2, 56.6]
metrics = [46.1, 49.8, 55.2, 56.2, 58.5]
# metrics = [[45.1, 49.7, 52.3, 55.2, 56.6], [46.1, 49.8, 55.2, 56.2, 58.5]]


training_data_percentages = [20, 40, 60, 80, 100]

# 创建一个折线图
plt.figure(figsize=(10, 6))  # 设置图形的大小
plt.plot(training_data_percentages, metrics, marker='o')  # 绘制折线图，'o'表示点的形状

# 添加标题和标签
# plt.title('Performance Metrics vs Training Data Percentage')
plt.xlabel('Training Data (%)')
plt.ylabel('Metric (%)')

# 显示图例
plt.legend(['F1', 'Hits@1', 'Acc'], loc='upper left')

# 显示网格（可选）
plt.grid(True)

# 显示图形
plt.show()