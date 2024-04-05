import json
import sys
import jsonlines
from tqdm import tqdm
import random
import re

def contains_chinese(text):
    # 匹配所有中文字符
    pattern = re.compile(r'[\u4e00-\u9fff]+')
    # 搜索字符串中是否有匹配的中文字符
    if pattern.search(text):
        return True
    else:
        return False

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
    data_open_file_utility = './data_open/Belle_open_source_train_Utility_V1.json'

    datas_open_file_utility = load_file(data_open_file_utility)

    # 将数组打乱掉
    random.shuffle(datas_open_file_utility)
    # datas_open_file_utility[:1000]

    num_all = 0;
    index = 0
    index1 = 0
    id_index = 0
    items = []

    for data in datas_open_file_utility:
        # if len(items) == 10000:
        #     break

        print(data)
        index1 += 1

        # 过滤输入长度的限制,长度限制8K
        if len(data['instruction']) + len(data['output']) > 2014:
            # # 恢复标准输出
            # sys.stdout = sys.__stdout__
            print(f"{index1} --------data['answer'] 过长，放弃治疗---------长度为:{len(data['instruction']) + len(data['output'])}------------")
            print()
            continue

        if not contains_chinese(data['output']):
            continue

        data = json.dumps(data, ensure_ascii=False)
        items.append(data)


    data_open_file_utility_save_train = './data_open_train/Belle_open_source_train_Utility_1W_train_V1.jsonl'
    data_open_file_utility_save_test = './data_open_train/Belle_open_source_train_Utility_1W_test_V1.jsonl'
    data_open_file_utility_save_dev = './data_open_train/Belle_open_source_train_Utility_1W_dev_V1.jsonl'
    data_open_file_utility_save = './data_open_train/Belle_open_source_train_Utility_all_V1.jsonl'
    items_train = items[:7000]
    items_test = items[7000:9000]
    items_dev = items[9000:10000]

    # file_save_path = data_open_file_utility_save_train

    store_json_per_line(items_train, data_open_file_utility_save_train)
    store_json_per_line(items_test, data_open_file_utility_save_test)
    store_json_per_line(items_dev, data_open_file_utility_save_dev)
    store_json_per_line(items, data_open_file_utility_save)


    print("end")





if __name__ == "__main__":
    print("\nstart:\n\n")
    main()
    print("\n\nend!!!\n\n")




