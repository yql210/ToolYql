import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


# 准备数据
training_data_percentages = [20, 40, 60, 80, 100]

metrics_6b_1 = [45.1, 49.7, 52.3, 55.2, 56.6]
metrics_13b_1 = [46.1, 49.8, 55.2, 56.2, 58.5]
# metrics = [[45.1, 49.7, 52.3, 55.2, 56.6], [46.1, 49.8, 55.2, 56.2, 58.5]]

metrics_6b_2 = [32.3, 39.2, 44.1, 46.6, 53]
metrics_13b_2 = [35.6, 44.5, 50.6, 49.6, 55.6]
# metrics = [[45.1, 49.7, 52.3, 55.2, 56.6], [46.1, 49.8, 55.2, 56.2, 58.5]]


# 创建一个包含两个子图的图表，1行2列
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
# fig, (ax1, ax2) = plt.subplots(1, 2)

# 设置matplotlib的字体
plt.rcParams['font.sans-serif'] = ['SimSun']  # 指定默认字体为SimHei
plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

# 设置全局字体大小
plt.rcParams.update({'font.size': 12})  # 设置为16磅

# # 设置x轴和y轴的刻度
# plt.xticks(np.arange(20, 100, 20))  # 从-1.5到1.5，步长为0.5
# plt.yticks(np.arange(30, 80, 10))  # 从0到10，步长为1
#
# # 设置x轴和y轴的刻度标签
# plt.xticks(np.arange(20, 120, 20), ['20%', '40%', '60%', '80%', '100%'])
# plt.yticks(np.arange(30, 90, 10), ['30', '40', '50', '60', '70', '80'])
#
# # 设置y轴的上下限
# plt.ylim(30, 60)


# 在第一个子图(ax1)中绘制正弦函数
ax1.plot(training_data_percentages, metrics_6b_1, label='NL2Cypher（ChatGLM3-6b）', marker='o')  # 绘制 折线图
ax1.plot(training_data_percentages, metrics_13b_1, label='NL2Cypher（Baichuan2-13b）', marker='s')  # 绘制 折线图
ax1.set_xlabel('训练数据集大小（%）', fontsize=12)
ax1.set_ylabel('执行准确率（%）', fontsize=12)
# 添加图例
ax1.legend(loc='lower right')
ax1.set_xticks(np.arange(20, 120, 20), ['20%', '40%', '60%', '80%', '100%'])
ax1.set_yticks(np.arange(30, 90, 10), ['30', '40', '50', '60', '70', '80'])
ax1.set_ylim(28, 62)


# 在第二个子图(ax2)中绘制余弦函数
ax2.plot(training_data_percentages, metrics_6b_2, label='NL2Cypher（ChatGLM3-6b）', marker='o')  # 绘制 折线图
ax2.plot(training_data_percentages, metrics_13b_2, label='NL2Cypher（Baichuan2-13b）', marker='s')  # 绘制 折线图
ax2.set_xlabel('训练数据集大小（%）', fontsize=12)
ax2.set_ylabel('逻辑准确率（%）', fontsize=12)
# 添加图例
ax2.legend(loc='lower right')
ax2.set_xticks(np.arange(20, 120, 20), ['20%', '40%', '60%', '80%', '100%'])
ax2.set_yticks(np.arange(30, 90, 10), ['30', '40', '50', '60', '70', '80'])
ax2.set_ylim(28, 62)



# 调整子图间的间距
plt.tight_layout()


# 获取当前时间
current_time = datetime.now()
# 将当前时间转换为字符串
time_str = current_time.strftime('%Y-%m-%d-%H-%M-%S')
# 保存为SVG格式
plt.savefig('./picture/train_data_NL_Cypher_' + time_str + '.svg')


# 显示图表
plt.show()