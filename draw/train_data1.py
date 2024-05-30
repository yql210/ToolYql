import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np



# 准备数据
training_data_percentages = [20, 40, 60, 80, 100]

metrics_6b = [32.3, 39.2, 44.1, 46.6, 53]
metrics_13b = [35.6, 44.5, 50.6, 49.6, 55.6]
# metrics = [[45.1, 49.7, 52.3, 55.2, 56.6], [46.1, 49.8, 55.2, 56.2, 58.5]]



# 设置matplotlib的字体
plt.rcParams['font.sans-serif'] = ['SimSun']  # 指定默认字体为SimHei
plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

# 设置全局字体大小
plt.rcParams.update({'font.size': 12})  # 设置为16磅

# 创建图表
# plt.figure(figsize=(10, 5))  # 设置图表大小

# # 去除x轴刻度线
# plt.gca().xaxis.set_tick_params(which='both', length=0)  # both指的是major and minor ticks
#
# # 去除y轴刻度线
# plt.gca().yaxis.set_tick_params(which='both', length=0)

# # 去除x轴刻度标签
# plt.gca().set_xticklabels([])
#
# # 去除y轴刻度标签
# plt.gca().set_yticklabels([])

# 设置x轴和y轴的刻度
plt.xticks(np.arange(20, 100, 20))  # 从-1.5到1.5，步长为0.5
plt.yticks(np.arange(30, 80, 10))  # 从0到10，步长为1

# 设置x轴和y轴的刻度标签
plt.xticks(np.arange(20, 120, 20), ['20%', '40%', '60%', '80%', '100%'])
plt.yticks(np.arange(30, 90, 10), ['30', '40', '50', '60', '70', '80'])

# 设置y轴的上下限
plt.ylim(30, 60)

# 绘制折线图
plt.plot(training_data_percentages, metrics_6b, label='NL2Cypher（ChatGLM3-6b）', marker='o')  # 绘制 折线图
plt.plot(training_data_percentages, metrics_13b, label='NL2Cypher（Baichuan2-13b）', marker='s')  # 绘制 折线图



# 添加标题和标签
# plt.title('Performance Metrics vs Training Data Percentage')
plt.xlabel('训练数据集大小（%）')
plt.ylabel('逻辑准确率（%）')

# # 显示网格（可选）
# plt.grid(True)

# 显示图表
plt.show()

