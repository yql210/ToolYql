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
    # for item in data:
    #     q_id = item["id"] if "id" in item else item["q_id"]
    #     final_results.setdefault(q_id, [])
    #     final_results[q_id].append(item)
    return data

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

    file_dev_path = './data_open_train/Belle_open_source_train_Utility_1W_dev_V1.jsonl'
    file_test_path = './data_open_train/Belle_open_source_train_Utility_1W_test_V1.jsonl'
    file_train_path = './data_open_train/Belle_open_source_train_Utility_1W_train_V1.jsonl'

    file_dev_save_path = './SArag_all/Belle_dev_train.jsonl'
    file_test_save_path = './SArag_all/Belle_test_train.jsonl'
    file_train_save_path = './SArag_all/Belle_train_train.jsonl'


    # input_data = load_all_files(file_dev_path)
    # file_save_path = file_dev_save_path

    # input_data = load_all_files(file_test_path)
    # file_save_path = file_test_save_path

    input_data = load_all_files(file_train_path)
    file_save_path = file_train_save_path

    index = 0
    index1 = 0
    id_index = 0
    items = []
    length = int(len(input_data) / 10) * 10

    for instance in input_data:

        if index1 == length:
            break

        index1 += 1

        output = ""

        output += "[No Retrieval]" + instance['output'] + instance['pred']

        conversation = {"instruction": instance['instruction'],
                        "cypher": '',
                        "answer": instance['output'],
                        "glm-4-answer": '',
                        "output": output,
                        "input": "",
                        "topic": "",
                        "Retrieval": '[No Retrieval]',
                        "isSup": '',
                        "isUtility": instance['pred'],
                        "id": "Belle_" + str(id_index),
                        "dataset_name": "Belle"}

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


