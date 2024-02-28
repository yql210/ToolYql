import os
from openai import OpenAI

client = OpenAI(
    api_key="sk-oifMRsZvyiS3VLMSJcTDcDIQbQEzi7PqDLnBJrzuXHUtjTjw",
    base_url="https://api.moonshot.cn/v1",
)

completion = client.chat.completions.create(
  model="moonshot-v1-8k",
  messages=[
    {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一些涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
    {"role": "user", "content": "给定一个指令和一个输出，评价响应是否看起来是对查询有帮助和信息丰富的答案，从1(最低)到5(最高)。我们称这个分数为感知效用。具体标准如下:5:响应对查询提供了一个完整的、非常详细的、翔实的响应，完全满足了信息需求。4:回复基本上满足了查询的需要，但还可以有一些小的改进，比如讨论更详细的信息，更好的回复结构，或者提高连贯性。3:响应是可以接受的，但需要一些重大的补充或改进，以满足用户的需求。2:响应仍然处理主请求，但它不完整或与查询无关。1 .回答几乎不切题或者完全不相关。\n"
                                "指令：2023年英国现任首相是谁?\n"
                                "输出：鲍里斯·约翰逊在2019年至2022年期间担任英国首相。"}
  ],
  temperature=0.2,
)

print(completion.choices[0].message)