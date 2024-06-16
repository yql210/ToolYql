from transformers import AutoTokenizer, AutoModelForCausalLM
from vllm import LLM, SamplingParams

# https://huggingface.co/selfrag/selfrag_llama2_7b
# model = LLM("selfrag/selfrag_llama2_7b", download_dir="/gscratch/h2lab/akari/model_cache", dtype="half")

# model = LLM("/data/noremove/huggingface/hub/models--selfrag--selfrag_llama2_7b/snapshots/190261383b0779ff66d2f95a73c7ad267d94b820", dtype="half")
# model = LLM("/data/result/selfrag/spcql/0309_self_rag_1.3b_epcoh_40/", dtype="half")
# model = LLM("/data/result/selfrag/spcql/0311_self_rag_1.3b_epcoh_5/", dtype="half")
model = LLM("/data/result/sarag/SArag_all/0405_sa_rag_1.3b_epcoh_3", dtype="half")


# model = LLM("/data/yuanql/model/modelscope/AI-ModelScope/chinese-llama-2-1.3b", dtype="half")

sampling_params = SamplingParams(temperature=0.50, top_p=1.0, max_tokens=512, skip_special_tokens=False)

def format_prompt(input, paragraph=None):
  prompt = "### Instruction:\n{0}\n\n### Response:\n".format(input)
  if paragraph is not None:
    prompt += "[Retrieval]<paragraph>{0}</paragraph>".format(paragraph)\

  # print(prompt)

  return prompt

# query_1 = "Leave odd one out: twitter, instagram, whatsapp."
query_1 = "列举出鲁迅的一个别名可以吗？"
query_2 = "100个空前最爱这个益智游戏都有什么属性标签呢?"
queries = [query_1, query_2]

preds = model.generate([format_prompt(query) for query in queries], sampling_params)
for pred in preds:
  print()
  print("Model prediction: {0}".format(pred.outputs[0].text))
  print()
# Model prediction: Twitter, Instagram, and WhatsApp are all social media platforms.[No Retrieval]WhatsApp is the odd one out because it is a messaging app, while Twitter and # Instagram are primarily used for sharing photos and videos.[Utility:5]</s> (this query doesn't require factual grounding; just skip retrieval and do normal instruction-following generation)
# Model prediction: Sure![Retrieval]<paragraph> ... (this query requires factual grounding, call a retriever)

# generate with retrieved passage
prompt = format_prompt("列举出鲁迅的一个别名可以吗？", paragraph="周做人")
preds = model.generate([prompt], sampling_params)
print([pred.outputs[0].text for pred in preds])
# ['[Relevant]Alpacas are considerably smaller than llamas, and unlike llamas, they were not bred to be working animals, but were bred specifically for their fiber.[Fully supported][Utility:5]</s>']


while True:
  user_input = input("请输入内容（输入 'exit' 退出）: ")

  # 检查用户是否输入了 'exit'
  if user_input.lower() == 'exit':
    print("退出程序。")
    break  # 退出循环
  else:
    # 处理用户输入的数据
    # print(f"你输入了: {user_input}")
    prompt = format_prompt(user_input)

    preds = model.generate([prompt], sampling_params)

    print([pred.outputs[0].text for pred in preds])

  user_input1 = input("！！请输入paragraph内容（输入 'exit' 退出）！！: ")

  # 检查用户是否输入了 'exit'
  if user_input.lower() == 'exit':
    print("退出程序。")
    break  # 退出循环
  else:
    # 处理用户输入的数据
    # print(f"你输入了: {user_input}")
    prompt = format_prompt(user_input, paragraph=user_input1)

    preds = model.generate([prompt], sampling_params)

    print([pred.outputs[0].text for pred in preds])


