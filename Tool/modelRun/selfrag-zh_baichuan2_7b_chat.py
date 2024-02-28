from transformers import AutoTokenizer, AutoModelForCausalLM
from vllm import LLM, SamplingParams

# https://huggingface.co/Aman/selfrag-zh_baichuan2_7b_chat
# model = LLM("Aman/selfrag-zh_baichuan2_7b_chat", dtype="half", trust_remote_code=True)
model = LLM("/data/noremove/huggingface/hub/models--Aman--selfrag-zh_baichuan2_7b_chat/snapshots/6825b988ae6d5c4ca7dcf906760e7b5e2a76d145", dtype="half", trust_remote_code=True)
sampling_params = SamplingParams(temperature=0.0, top_p=1.0, max_tokens=100, skip_special_tokens=False)

def format_prompt(input, paragraph=None):
    prompt = "### Instruction:\n{0}\n\n### Response:\n".format(input)
    if paragraph is not None:
        prompt += "[Retrieval]<paragraph>{0}</paragraph>".format(paragraph)
    return prompt

query_1 = "你好"
query_2 = "世界最高的山峰是什么？"
query_3 = "周杰伦演唱的歌曲那些？"
query_11 = "Leave odd one out: twitter, instagram, whatsapp."
query_22 = "Can you tell me the difference between llamas and alpacas?"
queries = [query_1, query_2, query_3, query_11, query_22]

preds = model.generate([format_prompt(query) for query in queries], sampling_params)
for pred in preds:
    print("Model prediction: {0}".format(pred.outputs[0].text))
# Model prediction: 你好~有什么我可以帮忙的吗？(*^__^*) ">Hello again friendlier than before :) ">Surely you can help me solve my problem :) ">No problem friend :) ">Greatly appreciated friend :) ">Take care friend :) ">Bye friend :) ">See you later friend :) ">Goodbye friend :) ">See you tomorrow friend :) ">Goodnight friend :) ">Sleep well friend :) ">Goodbye friend :) ">See you
# Model prediction: 世界最高的山峰是珠穆朗玛峰29979英尺/8986米2021202220222022202220222022202220222022202220222022202220222022202220222022202
# Model prediction: 周杰伦是一位著名的华语流行歌手兼词曲创作者2000年代初开始发片2003年初初成名2000年代初开始发片2003年初初成名2007年获得全球华语音乐榜中榜最佳男歌手2010年获得MTV全球华语音乐盛典最佳男歌手2017年获得华语音乐盛典终身成就奖2019年获得KBS全球华语音乐盛典终身成就奖2021年获得Q Music
# Model prediction: Whatsapp odd one out because it is not a social media platform like twitter or instagram but a messaging app used worldwide for communication purposes alone instead of being a platform where users share content like photos or status updates like instagram or tweets do instead of being a platform where users communicate via text message like whatsapp instead of being a platform where users communicate via voice message like whatsapp instead of being a platform where users communicate via video message like whatsapp instead of being a platform where users
# Model prediction: Llamas vs Alpaca: Difference Between Lambs vs Alpaca Wool Fibers [Video] [12:25] [12:25] [12:25] [12:25] [12:25] [12:25] [12:25] [12:25] [12:25] [12:25] [12:25] [12

print("end")
