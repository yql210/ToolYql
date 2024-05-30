import matplotlib.pyplot as plt

# 准备数据
x = [20, 40, 60, 80, 100]  # 假设这是训练数据的百分比
y1 = [100, 90, 80, 70, 60]  # 假设这是F1分数
y2 = [100, 95, 90, 85, 80]  # 假设这是准确率（Acc）
y3 = [100, 98, 96, 94, 92]  # 假设这是Hits@1

# 创建图表
plt.figure(figsize=(10, 5))  # 设置图表大小

# 绘制折线图
plt.plot(x, y1, label='F1 Score', marker='o')  # 绘制F1分数折线图
plt.plot(x, y2, label='Accuracy', marker='s')  # 绘制准确率折线图
plt.plot(x, y3, label='Hits@1', marker='^')   # 绘制Hits@1折线图

# 添加图例
plt.legend()

# 添加标题和标签
plt.title('Performance Metrics vs Training Data Percentage')
plt.xlabel('Training Data (%)')
plt.ylabel('Metric (%)')

# 显示网格（可选）
plt.grid(True)

# 显示图表
plt.show()