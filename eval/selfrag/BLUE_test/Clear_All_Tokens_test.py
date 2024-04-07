import re


def clear_all_tokens(model_answer):
    # 使用正则表达式匹配所有的 [ ] 包含的内容
    # 匹配的模式为 $$.*?$$，其中：
    # $$ 表示匹配左方括号 [    # .*? 表示匹配任意字符，. 表示任意字符，* 表示0次或多次，? 使得匹配变为非贪婪模式    # $$ 表示匹配右方括号 ]

    # [# 正则表达式 - 语法](https://www.runoob.com/regexp/regexp-syntax.html)
    # [正则表达式-在线测试工具](https://www.jyshare.com/front-end/854/)

    return re.sub(r'\[.*?]', '', model_answer)


# 示例字符串
input_str = "这是一个示例字符串，包含[方括号]和[带有内容的方括号]。"
output_str = clear_all_tokens(input_str)

print(output_str)

# 编译正则表达式模式
pattern = re.compile(r'\[.*?]')

# 查找所有匹配项
matches = pattern.findall(input_str)

print(matches)