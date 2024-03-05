from transformers import AutoTokenizer, AutoModelForCausalLM
from vllm import LLM, SamplingParams

# https://huggingface.co/selfrag/selfrag_llama2_7b
# model = LLM("selfrag/selfrag_llama2_7b", download_dir="/gscratch/h2lab/akari/model_cache", dtype="half")

model = LLM("/data/noremove/huggingface/hub/models--selfrag--self_rag_critic/snapshots/6b453dff820203db95e19ffd9151054737655e54", dtype="half")

sampling_params = SamplingParams(temperature=0.0, top_p=1.0, max_tokens=100, skip_special_tokens=False)

def format_prompt(input, paragraph=None):
  prompt = "### Instruction:\n{0}\n\n### Response:\n".format(input)
  if paragraph is not None:
    prompt += "[Retrieval]<paragraph>{0}</paragraph>".format(paragraph)\

  print(prompt)

  return prompt

query_1 = "Leave odd one out: twitter, instagram, whatsapp."
# query_1 = "列举出鲁迅的一个别名可以吗？"
query_2 = "Can you tell me the difference between llamas and alpacas?"
queries = [query_1, query_2]

preds = model.generate([format_prompt(query) for query in queries], sampling_params)
for pred in preds:
  print("Model prediction: {0}".format(pred.outputs[0].text))
# Model prediction: Twitter, Instagram, and WhatsApp are all social media platforms.[No Retrieval]WhatsApp is the odd one out because it is a messaging app, while Twitter and # Instagram are primarily used for sharing photos and videos.[Utility:5]</s> (this query doesn't require factual grounding; just skip retrieval and do normal instruction-following generation)
# Model prediction: Sure![Retrieval]<paragraph> ... (this query requires factual grounding, call a retriever)

# # generate with retrieved passage
# prompt = format_prompt("列举出鲁迅的一个别名可以吗？", paragraph="周树人")
# preds = model.generate([prompt], sampling_params)
# print([pred.outputs[0].text for pred in preds])
# # ['[Relevant]Alpacas are considerably smaller than llamas, and unlike llamas, they were not bred to be working animals, but were bred specifically for their fiber.[Fully supported][Utility:5]</s>']
