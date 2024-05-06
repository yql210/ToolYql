import json
import sys
import jsonlines
from tqdm import tqdm
import random


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



    file_train_path = './SArag_all/SArag_train_train.jsonl'

    file_train_save_path = './SArag_all/SArag_train_train_only_output.jsonl'



    input_datas = load_file(file_train_path)
    file_save_path = file_train_save_path

    items = []

    out_index = int(len(input_datas))




    for data in input_datas:
        if data['Retrieval'] == "[Retrieval]":
            data['output'] = data['glm-4-answer']
        else:
            data['output'] = data['answer']
        data = json.dumps(data, ensure_ascii=False)
        items.append(data)


    # # 将数组打乱掉
    # random.shuffle(items)

    store_json_per_line(items, file_save_path)
    print('end')


if __name__ == "__main__":
    print("\nstart:\n\n")
    main()
    print("\n\nend!!!\n\n")




