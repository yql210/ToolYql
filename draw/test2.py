import matplotlib.pyplot as plt
import numpy as np

# 准备数据
x = np.linspace(0, 10, 100)  # 生成100个从0到10的等差数列
y = np.sin(x)  # 以x为自变量的正弦函数值

# 创建图表
plt.figure(figsize=(8, 6))

# 绘制折线图
plt.plot(x, y)

# 设置x轴和y轴的范围
plt.xlim(0, 10)
plt.ylim(-1.5, 1.5)

# 设置x轴和y轴的刻度
plt.xticks(np.arange(0, 11, 1))  # 从0到10，步长为1
plt.yticks(np.arange(-1.5, 1.6, 0.5))  # 从-1.5到1.5，步长为0.5

# 设置x轴和y轴的刻度标签
plt.xticks(np.arange(0, 11, 1), ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
plt.yticks(np.arange(-1.5, 1.6, 0.5), ['-1.5', '-1.0', '-0.5', '0', '0.5', '1.0', '1.5'])

# 设置x轴和y轴的标题
plt.xlabel('横坐标')
plt.ylabel('纵坐标')

# 显示网格（可选）
plt.grid(True)

# 显示图表
plt.show()