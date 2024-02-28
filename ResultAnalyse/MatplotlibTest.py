import matplotlib.pyplot as plt

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimSun']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 示例数据
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# 使用 Seaborn 绘制折线图
plt.plot(x, y, label='数据系列1')

# 添加图例
plt.legend()

# 设置图表标题和轴标签
plt.title('折线图')
plt.xlabel('X中国')
plt.ylabel('Y')

# 显示图表
plt.show()

# # -*- coding: utf-8 -*-
#
# import matplotlib.pyplot as plt
# import numpy as np
#
# # 解决中文显示问题
# plt.rcParams['font.sans-serif'] = ['SimSun']  # 指定默认字体
# plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
#
# x = np.linspace(-8, 8, 1024)
# y1 = 0.618 * np.abs(x) - 0.8 * np.sqrt(64 - x ** 2)
# y2 = 0.618 * np.abs(x) + 0.8 * np.sqrt(64 - x ** 2)
# plt.plot(x, y1, color='r')
# plt.plot(x, y2, color='r')
# plt.title("爱你一万年")
# plt.show()