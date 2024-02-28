# pip install zhipuai 请先在终端进行安装

from zhipuai import ZhipuAI

client = ZhipuAI(api_key="2178e91663c1f74a6f61b53eef5abd82.4sk2Una0UGk3nODJ")

response = client.chat.completions.create(
    model="glm-3-turbo",
    messages=[
        {
            "role": "user",
            # "content": "帮我写10个问句，意思和示例一致：\n歌曲兰亭序所属的音乐专辑是那个？"
            "content": "给定一个指令和一个输出，评价响应是否看起来是对查询有帮助和信息丰富的答案，从1(最低)到5(最高)。"
                       "我们称这个分数为有效性。具体标准如下:"
                       "5:响应对查询提供了一个完整的、非常详细的、翔实的响应，完全满足了信息需求。"
                       "4:回复基本上满足了查询的需要，但还可以有一些小的改进，比如讨论更详细的信息，更好的回复结构，或者提高连贯性。"
                       "3:响应是可以接受的，但需要一些重大的补充或改进，以满足用户的需求。"
                       "2:响应仍然处理主请求，但它不完整或与查询无关。"
                       "1 .回答几乎不切题或者完全不相关。\n"
                        "指令：2023年英国现任首相是谁?\n"
                        "输出：鲍里斯·约翰逊在2019年至2022年期间担任英国首相。"
            # "content": "你好"
        }
    ],
    top_p=0.7,
    temperature=0.95,
    max_tokens=1024,
    stream=True,
)
for trunk in response:
    print(trunk.choices[0].delta.content, end="")

print("\nend")
