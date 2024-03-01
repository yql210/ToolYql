import sys
import time

# 打开一个文件用于写入
with open('output.txt', 'a', encoding='utf-8') as file:
    # 将标准输出重定向到文件
    sys.stdout = file
    print('Hello, World!')
    # 现在输出会同时显示在屏幕上和写入到文件中


with open('output.txt', 'a', encoding='utf-8') as file:
    # 将标准输出重定向到文件
    sys.stdout = file
    print('Hello, World!')
    # 现在输出会同时显示在屏幕上和写入到文件中


with open('output_error.txt', 'a', encoding='utf-8') as file:
    # 将标准输出重定向到文件
    sys.stdout = file
    print('Hello, World!')

# 恢复标准输出
sys.stdout = sys.__stdout__


print("start")
time.sleep(60)  # 延迟60秒

print("end")
