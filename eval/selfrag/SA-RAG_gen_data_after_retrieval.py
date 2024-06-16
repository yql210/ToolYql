from vllm import LLM, SamplingParams
import json
import sys
import jsonlines
from tqdm import tqdm


def read_large_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            yield json.loads(line)


def store_json_per_line(json_data, output_file):
    with open(output_file, "a", encoding="utf-8") as file:
        for item in json_data:
            # json.dump(item, file, ensure_ascii=False, indent=4)
            file.write(item + "\n")


def load_jsonlines(file):
    with jsonlines.open(file, 'r') as jsonl_f:
        lst = [obj for obj in jsonl_f]
    return lst


def load_json(fname, mode="r", encoding="utf8"):
    if "b" in mode:
        encoding = None
    with open(fname, mode=mode, encoding=encoding) as f:
        return json.load(f)

def load_file(file_name):
    print(file_name)
    if file_name.endswith(".json"):
        data = json.load(open(file_name, encoding="utf-8"))
    elif file_name.endswith(".jsonl"):
        data = load_jsonlines(file_name)
    else:
        if ".json_" in file_name:
            data = json.load(open(file_name))
        elif ".jsonl_" in file_name:
            data = load_jsonlines(file_name)
    return data


def load_all_files(file_paths):
    final_results = {}
    # for fp in file_paths:
    data = load_file(file_paths)
    for item in data:
        q_id = item["id"] if "id" in item else item["q_id"]
        final_results.setdefault(q_id, [])
        final_results[q_id].append(item)
    return final_results

def format_prompt(input, paragraph=None):
  prompt = "### Instruction:\n{0}\n\n### Response:\n".format(input)
  if paragraph is not None:
    # prompt += "[Retrieval]<paragraph>{0}</paragraph>".format(paragraph)\
    prompt += "<paragraph>{0}</paragraph>".format(paragraph)\
    # prompt += "<paragraph></paragraph>"\
    # prompt += "[Retrieval]<paragraph></paragraph>"\
  # else:
  #   prompt += "<paragraph></paragraph>"

  # print(prompt)
  return prompt

# 作为可以根据问题和知识库的信息完美的生成可以通过图灵测试回答的知识库检索型对话专家，回答的受众是对知识库信息出现在回答中要求很高，并且回答精炼。提供的回答高度契合知识库信息，语言流畅，无关信息不要回复。在回答时，请扮演一个儒雅的老者，根据知识库中的信息给出确切回复，回复一段或者一句话。\n问题：+ data['query'] +  \n知识：+ str(data['answer'])

# def format_prompt(input, paragraph=None):
#   prompt = "作为可以根据问题和知识库的信息完美的生成可以通过图灵测试回答的知识库检索型对话专家，回答的受众是对知识库信息出现在回答中要求很高，并且回答精炼。提供的回答高度契合知识库信息，语言流畅，无关信息不要回复。在回答时，请扮演一个儒雅的老者，根据知识库中的信息给出确切回复，回复一段或者一句话。\n问题：{0} ".format(input)
#   if paragraph is not None:
#     prompt += "\n知识：{0}。".format(paragraph)\
#
#   # print(prompt)
#   return prompt




def main():
    file_output = './FINAL_OUTPUT_PATH/output.txt'
    file_output_toLong = './FINAL_OUTPUT_PATH/output_toLong.txt'
    file_output_error = './FINAL_OUTPUT_PATH/output_error.txt'

    # with open(file_output, 'a', encoding='utf-8') as file:
    #     # 将标准输出重定向到文件
    #     sys.stdout = file
    #     print("----------start-------------------")
    #
    # # 恢复标准输出
    # sys.stdout = sys.__stdout__
    # print("----------start-------------------")

    # model_train_path = '0405_sa_rag_1.3b_epcoh_20'
    # model_train_path = '0405_sa_rag_1.3b_epcoh_5'
    # model_train_path = '0405_sa_rag_1.3b_epcoh_10'
    # model_train_path = '0405_sa_rag_1.3b_epcoh_3'
    # model_train_path = '0405_sa_rag_1.3b_epcoh_40'

    # 开始测试数据集对其影响
    # model_train_path = '0410_sa_rag_1.3b_epcoh_3_data_0_2'
    # model_train_path = '0410_sa_rag_1.3b_epcoh_3_data_0_4'
    # model_train_path = '0410_sa_rag_1.3b_epcoh_3_data_0_6'
    # model_train_path = '0410_sa_rag_1.3b_epcoh_3_data_0_8'
    # model_train_path = '0410_sa_rag_1.3b_epcoh_3_data_alone_spcql'

    # model_train_path = '0506_sa_rag_1.3b_epcoh_3_only_output'

    # model_train_path = '0530_sa_rag_1.3b_epcoh_3_no_retrieval'
    model_train_path = '0530_sa_rag_1.3b_epcoh_3_no_label'

    file_test_path = './sa-self-gen-data/' + model_train_path + '.jsonl'
    file_test_path = './sa-self-data/SArag_test_train.jsonl'

    # file_save_path = './sa-self-gen-data-after-retrieval/' + model_train_path + '_after_retrieval.jsonl'
    # file_save_path = './sa-self-gen-data-after-retrieval/0530_' + model_train_path + '_no_retrieval_after_retrieval.jsonl'
    # file_save_path = './sa-self-gen-data-after-retrieval/0530_' + model_train_path + '_no_retrieval_after_retrieval_1.jsonl'
    file_save_path = './sa-self-gen-data-after-retrieval/0530_' + model_train_path + '_all_retrieval_after_retrieval_2.jsonl'

    model_path = '/data/result/sarag/SArag_all/' + model_train_path

    # model_path = '/data/yuanql/model/modelscope/AI-ModelScope/chinese-llama-2-1.3b'
    # file_test_path = './sa-self-gen-data/chinese-llama-2-1.3b.jsonl'
    # file_save_path = './sa-self-gen-data-after-retrieval/chinese-llama-2-1.3b.jsonl'

    # model_path = '/data/yuanql/model/modelscope/ChineseAlpacaGroup/chinese-llama-2-7b'
    # file_test_path = './sa-self-gen-data/chinese-llama-2-7b.jsonl'
    # file_save_path = './sa-self-gen-data-after-retrieval/chinese-llama-2-7b.jsonl'

    # model_path = '/data/yuanql/model/modelscope/ChineseAlpacaGroup/chinese-llama-2-13b'
    # file_test_path = './sa-self-gen-data/chinese-llama-2-13b.jsonl'
    # file_save_path = './sa-self-gen-data-after-retrieval/chinese-llama-2-13b.jsonl'


    model = LLM(model_path, dtype="half")
    sampling_params = SamplingParams(temperature=0.0, top_p=1.0, max_tokens=512, skip_special_tokens=False)

    input_datas = load_file(file_test_path)

    index = 0
    index1 = 0
    id_index = 0
    items = []
    # length = int(len(input_datas) / 10) * 10

    for data in input_datas:
        print(index1)
        # print(data)

        # if index1 == length:
        #     break

        index1 += 1

        # if data['Retrieval'] == '[No Retrieval]':
        #     continue
        if data['Retrieval'] == "[Retrieval]":
            prompt = format_prompt(data['instruction'], paragraph=data['answer'])
            # prompt = format_prompt(data['instruction'], '')
        else:
            prompt = format_prompt(data['instruction'])

        preds = model.generate([prompt], sampling_params)

        data['SA_RAG_data'] = [pred.outputs[0].text for pred in preds]

        data = json.dumps(data, ensure_ascii=False)
        items.append(data)

        index += 1

        if index == 500:
            store_json_per_line(items, file_save_path)
            index = 0
            items = []
            # with open(file_output, 'a', encoding='utf-8') as file:
            #     # 将标准输出重定向到文件
            #     sys.stdout = file
            print("--------------" + str(index1) + "----------------")

    store_json_per_line(items, file_save_path)
    # with open(file_output, 'a', encoding='utf-8') as file:
    #     # 将标准输出重定向到文件
    #     sys.stdout = file
    #     print("--------------" + str(index1) + "----------------")
    #     print(index1)
    #     print("\n----------end-------------------")


if __name__ == "__main__":
    print("\nstart:\n\n")
    main()
    print("\n\nend!!!\n\n")





