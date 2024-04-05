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

    with open(file_output, 'a', encoding='utf-8') as file:
        # 将标准输出重定向到文件
        sys.stdout = file
        print("----------start-------------------")

    # 恢复标准输出
    sys.stdout = sys.__stdout__
    print("----------start-------------------")

    # file_dev_path = 'E:\\a_search\\github\\ToolYql\\data\\SpCQLToSelfRAG\\DataFromGlm4ToSelfRAG\\save_all\\SpCQL_dev_SelfRAG_V1_save.jsonl'
    file_dev_path = './save_all/SpCQL_dev_SelfRAG_V1_save.jsonl'
    file_test_path = './save_all/SpCQL_test_SelfRAG_V1_save.jsonl'
    file_train_path = './save_all/SpCQL_train_SelfRAG_V1_save.jsonl'

    # retrieval_file_dev_path = './INITIAL_RETRIEVAL_TOKEN_OUTPUT/SpCQL_dev_Retrieval_V1.json'
    # retrieval_file_test_path = './INITIAL_RETRIEVAL_TOKEN_OUTPUT/SpCQL_test_Retrieval_V1.json'
    # retrieval_file_train_path = './INITIAL_RETRIEVAL_TOKEN_OUTPUT/SpCQL_train_Retrieval_V1.json'

    utility_file_dev_path = './INITIAL_UTILITY_TOKEN_OUTPUT/SpCQL_dev_Utility_V1.json'
    utility_file_test_path = './INITIAL_UTILITY_TOKEN_OUTPUT/SpCQL_test_Utility_V1.json'
    utility_file_train_path = './INITIAL_UTILITY_TOKEN_OUTPUT/SpCQL_train_Utility_V1.json'

    # file_dev_save_path = './selfrag_all/SpCQL_dev_train_V1.jsonl'
    # file_test_save_path = './selfrag_all/SpCQL_test_train_V1.jsonl'
    # file_train_save_path = './selfrag_all/SpCQL_train_train_V1.jsonl'

    isSup_file_dev_path = './SArag_isSup/SpCQL_dev_train_V1.jsonl'
    isSup_file_test_path = './SArag_isSup/SpCQL_test_train_V1.jsonl'
    isSup_file_train_path = './SArag_isSup/SpCQL_train_train_V1.jsonl'

    file_dev_save_path = './SArag_all/SpCQL_dev_train.jsonl'
    file_test_save_path = './SArag_all/SpCQL_test_train.jsonl'
    file_train_save_path = './SArag_all/SpCQL_train_train.jsonl'

    input_data = load_all_files(file_dev_path)
    utility_data = load_all_files(utility_file_dev_path)
    isSup_data = load_all_files(isSup_file_dev_path)
    file_save_path = file_dev_save_path

    # input_data = load_all_files(file_test_path)
    # utility_data = load_all_files(utility_file_test_path)
    # isSup_data = load_all_files(isSup_file_test_path)
    # file_save_path = file_test_save_path

    # input_data = load_all_files(file_train_path)
    # utility_data = load_all_files(utility_file_train_path)
    # isSup_data = load_all_files(isSup_file_train_path)
    # file_save_path = file_train_save_path

    processed_data = []

    need_retrieval_initial_stats = []
    need_retrieval_multi_stats = []
    utility_stats = []
    groundness_stats = []
    relevance_stats = []

    index = 0
    index1 = 0
    id_index = 0
    items = []
    length = int(len(input_data) / 10) * 10

    for q_id, instance in tqdm(input_data.items()):

        if index1 == length:
            break

        index1 += 1

        # if index1 == 15:
        #     break

        # if index1 < 1400:
        #     index1 += 1
        #     continue

        # 过滤输入长度的限制,长度限制8K
        if len(instance[0]['answer']) > 8192:
            # 恢复标准输出
            sys.stdout = sys.__stdout__
            print(f"{index1} --------data['answer'] 过长，放弃治疗---------长度为:{len(instance[0]['answer'])}------------")
            print()
            print()
            print()
            with open(file_output_toLong, 'a', encoding='utf-8') as file:
                # 将标准输出重定向到文件
                sys.stdout = file
                print(f"{index1} --------data['answer'] 过长，放弃治疗---------长度为:{len(instance[0]['answer'])}------------")
                print()
            continue

        # 回复为ERROR的限制或者为空的限制
        if instance[0]['output'] == "ERROR" or instance[0]['output'] == "":
            # 恢复标准输出
            sys.stdout = sys.__stdout__
            print(f"{index1} --------回复为ERROR的限制或者为空的限制---------长度为{len(instance[0]['answer'])}------------")
            print("问题：" + instance[0]['query'] + "\n知识：" + str(instance[0]['answer']) + "\n回复:" + instance[0]['glm-4-answer'])
            print()
            print()
            with open(file_output_error, 'a', encoding='utf-8') as file:
                # 将标准输出重定向到文件
                sys.stdout = file
                print(f"{index1} --------回复为ERROR的限制或者为空的限制---------长度为{len(instance[0]['answer'])}------------")
                print("问题：" + instance[0]['query'] + "\n知识：" + str(instance[0]['answer']) + "\n回复:" + instance[0]['glm-4-answer'])
                print()
                print()
            continue

        output = ""

        if instance[0]['output'] != isSup_data[q_id][0]['output']:
            print("==========================================================")
            break

        if instance[0]['output'] != utility_data[q_id][0]['output']:
            print("==========================================================")
            break




        output += "[Retrieval]" + "<paragraph>{}</paragraph>".format(
            str(instance[0]['answer'])) + instance[0]['output'] + isSup_data[q_id][0]['isSup'] + utility_data[q_id][0]['pred']

        conversation = {"instruction": instance[0]['instruction'],
                        "cypher": instance[0]['cypher'],
                        "answer": str(instance[0]['answer']),
                        "glm-4-answer": instance[0]['output'],
                        "output": output,
                        "input": "",
                        "topic": "",
                        "Retrieval": '[Retrieval]',
                        "isSup": isSup_data[q_id][0]['isSup'],
                        "isUtility": utility_data[q_id][0]['pred'],
                        "id": "SpCQL_" + str(id_index),
                        "dataset_name": "SpCQL"}

        id_index += 1

        conversation = json.dumps(conversation, ensure_ascii=False)
        items.append(conversation)
        # print(conversation)
        index += 1

        if index == 500:
            store_json_per_line(items, file_save_path)
            index = 0
            items = []
            with open(file_output, 'a', encoding='utf-8') as file:
                # 将标准输出重定向到文件
                sys.stdout = file
                print("--------------" + str(index1) + "----------------")

    store_json_per_line(items, file_save_path)
    with open(file_output, 'a', encoding='utf-8') as file:
        # 将标准输出重定向到文件
        sys.stdout = file
        print("--------------" + str(index1) + "----------------")
        print(index1)
        print("\n----------end-------------------")





    with open(file_output, 'a', encoding='utf-8') as file:
        # 将标准输出重定向到文件
        sys.stdout = file
        print("\n----------end-------------------")

    # 恢复标准输出
    sys.stdout = sys.__stdout__
    print("\n----------end-------------------")



if __name__ == "__main__":
    print("\nstart:\n\n")
    main()
    print("\n\nend!!!\n\n")




