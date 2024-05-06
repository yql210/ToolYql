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
    prompt += "[Retrieval]<paragraph>{0}</paragraph>".format(paragraph)\

  # print(prompt)
  return prompt




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
    model_train_path = '0410_sa_rag_1.3b_epcoh_3_data_alone_spcql'

    file_test_path = './sa-self-data/SArag_test_train.jsonl'

    file_save_path = './sa-self-gen-data/' + model_train_path + '.jsonl'

    model_path = '/data/result/sarag/SArag_all/' + model_train_path

    # model_path = '/data/yuanql/model/modelscope/AI-ModelScope/chinese-llama-2-1.3b'
    # file_save_path = './sa-self-gen-data/chinese-llama-2-1.3b.jsonl'

    model_path = '/data/yuanql/model/modelscope/ChineseAlpacaGroup/chinese-llama-2-7b'
    file_save_path = './sa-self-gen-data/chinese-llama-2-7b.jsonl'

    # model_path = '/data/yuanql/model/modelscope/ChineseAlpacaGroup/chinese-llama-2-13b'
    # file_save_path = './sa-self-gen-data/chinese-llama-2-13b.jsonl'


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

        if index1 < 2501:
            continue

        prompt = format_prompt(data['instruction'])

        preds = model.generate([prompt], sampling_params)

        data['SA_RAG_data_no_ret'] = [pred.outputs[0].text for pred in preds]

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





