import seaborn as sns
import matplotlib.pyplot as plt

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimSun']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 示例数据
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# 使用 Seaborn 绘制折线图
sns.lineplot(x=x, y=y)

# 可选：设置图表标题和轴标签
plt.title('折线图')
plt.xlabel('X中国')
plt.ylabel('Y')

# 显示图表
plt.show()