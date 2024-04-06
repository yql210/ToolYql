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

    # file_path = './sa-self-gen-data/0405_sa_rag_1.3b_epcoh_20.jsonl'
    file_path = './sa-self-gen-data/0405_sa_rag_1.3b_epcoh_5.jsonl'

    input_datas = load_file(file_path)

    # 正面标签： `[Retrieval]`
    # 负面标签： `[No Retrieval]`
    TP = 0 # 原始：正面    预测：正面
    FN = 0 # 原始：正面    预测：负面
    FP = 0 # 原始：负面    预测：正面
    TN = 0 # 原始：负面    预测：负面
    error_zheng = 0
    error_fu = 0

    num_all_zheng = 0
    num_all_fu = 0

    for data in input_datas:
        # print(data)

        if data['Retrieval'] == "[Retrieval]":
            if "[Retrieval]" in data['SA_RAG_data_no_ret'][0]:
                TP += 1
            elif "[No Retrieval]" in data['SA_RAG_data_no_ret'][0]:
                FN += 1
            else:
                error_zheng += 1

            num_all_zheng += len(data['SA_RAG_data_no_ret'])


        elif data["Retrieval"] == "[No Retrieval]":
            if "[Retrieval]" in data['SA_RAG_data_no_ret'][0]:
                FP += 1
            elif "[No Retrieval]" in data['SA_RAG_data_no_ret'][0]:
                TN += 1
            else:
                error_fu += 1

            num_all_fu += len(data['SA_RAG_data_no_ret'])

    print("TP: ", TP)
    print("FN: ", FN)
    print("FP: ", FP)
    print("TN: ", TN)
    print("Error Zheng: ", error_zheng)
    print("Error Fu: ", error_fu)
    print("num_all_zheng: ", num_all_zheng)
    print("num_all_fu: ", num_all_fu)



if __name__ == "__main__":
    print("\nstart:\n\n")
    main()
    print("\n\nend!!!\n\n")





