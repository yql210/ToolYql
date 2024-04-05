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

def count_true(answer, output):
    """
    统计gold_answer与model_answer之间进行对比的相关数据
    :param gold_answer: 最原始的数据，即标准数据
    :param model_answer:  模型产生的数据，即生成数据
    :return: {'count_gold_num': 3, 'count_model_num': 4, 'count_model_num_true': 3, 'count_model_num_false': 1,
                'length_gold': 3, 'length_model': 3, 'set_isEmpty': True}
    """
    count_num = 0
    count_num_num = 0
    # count_model_num_true = 0
    # count_model_num_false = 0

    result = '[No support / Contradictory]'

    # # 创建一个空集合用于存储唯一的value键
    # gold_value_set = set()

    for dict_answer in answer:
        # 假设每个字典只有一个键值对
        for key, value in dict_answer.items():
            try:
                if str(value) in output:
                    count_num_num += 1
                count_num += 1
            except Exception as e:
                print(e)

    if count_num_num > 0:
        result = '[Partially supported]'

    if count_num == count_num_num:
        result = '[Fully supported]'

    if count_num == 0:
        result = '[Fully supported]'

    return result


def main():
    file_dev_path = './save_all/SpCQL_dev_SelfRAG_V1_save.jsonl'
    file_test_path = './save_all/SpCQL_test_SelfRAG_V1_save.jsonl'
    file_train_path = './save_all/SpCQL_train_SelfRAG_V1_save.jsonl'

    file_dev_save_path = './SArag_isSup/SpCQL_dev_train.jsonl'
    file_test_save_path = './SArag_isSup/SpCQL_test_train.jsonl'
    file_train_save_path = './SArag_isSup/SpCQL_train_train.jsonl'

    # data_open_file = file_dev_path
    # file_save_path = file_dev_save_path

    # data_open_file = file_test_path
    # file_save_path = file_test_save_path

    data_open_file = file_train_path
    file_save_path = file_train_save_path

    datas = load_file(data_open_file)

    num_partially = 0
    num_not_support = 0
    num_support = 0
    items = []

    for data in datas:

        answer = data['answer']
        output = data['output']

        result = count_true(answer, output)

        if result == '[Fully supported]':
            num_support += 1

        if result == '[Partially supported]':
            num_partially += 1

        if result == '[No support / Contradictory]':
            num_not_support += 1

        data['isSup'] = result
        data = json.dumps(data, ensure_ascii=False)
        items.append(data)

        print(data)

    print("[Fully supported]: ", num_support)
    print("[Partially supported]: ", num_partially)
    print("[No support / Contradictory]: ", num_not_support)

    store_json_per_line(items, file_save_path)

    print("end")

if __name__ == "__main__":
    print("\nstart:\n\n")
    main()
    print("\n\nend!!!\n\n")




