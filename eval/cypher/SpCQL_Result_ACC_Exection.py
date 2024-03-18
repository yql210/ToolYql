import json
import sys
import time
import func_timeout
from func_timeout import func_set_timeout
from threading import Thread
from py2neo import Graph, NodeMatcher, RelationshipMatcher
import jsonlines
import ast


def read_large_json_to_list(file_path):
    data_list = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            data_list.append(json.loads(line))
    return data_list


def read_large_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            yield json.loads(line)


def store_json_per_line(json_data, output_file):
    with open(output_file, "a", encoding="utf-8") as file:
        for item in json_data:
            # json.dump(item, file, ensure_ascii=False, indent=4)
            file.write(item + "\n")


def load_json(fname, mode="r", encoding="utf8"):
    if "b" in mode:
        encoding = None
    with open(fname, mode=mode, encoding=encoding) as f:
        return json.load(f)


def load_jsonlines(file):
    with jsonlines.open(file, 'r') as jsonl_f:
        lst = [obj for obj in jsonl_f]
    return lst


def count_true(gold_answer, model_answer):
    """
    统计gold_answer与model_answer之间进行对比的相关数据
    :param gold_answer: 最原始的数据，即标准数据
    :param model_answer:  模型产生的数据，即生成数据
    :return: {'count_gold_num': 3, 'count_model_num': 4, 'count_model_num_true': 3, 'count_model_num_false': 1,
                'length_gold': 3, 'length_model': 3, 'set_isEmpty': True}
    """
    count_gold_num = 0
    count_model_num = 0
    count_model_num_true = 0
    count_model_num_false = 0

    length_gold = len(gold_answer)
    length_model = len(model_answer)

    # 创建一个空集合用于存储唯一的value键
    gold_value_set = set()

    for dict_gold_answer in gold_answer:
        # 假设每个字典只有一个键值对
        for key, value in dict_gold_answer.items():
            try:
                # 将value值添加到集合中
                gold_value_set.add(str(value))
                count_gold_num += 1
            except Exception as e:
                print(e)

    for dict_model_answer in model_answer:
        for key, value in dict_model_answer.items():
            count_model_num += 1
            if str(value) in gold_value_set:
                count_model_num_true += 1
                gold_value_set.remove(str(value))
            else:
                count_model_num_false += 1

    if count_gold_num != length_gold:
        print("原始数据集中，length_gold与count_gold_num个数不同。分别是： ", count_gold_num, " --", length_gold)
        # time.sleep(10)

    if count_model_num != length_model:
        print("在生成的数据集中，length_model与count_model_num个数不同。分别是： ", count_model_num, " --", length_model)
        # time.sleep(10)

    result = {}
    result['count_gold_num'] = count_gold_num
    result['count_model_num'] = count_model_num
    result['count_model_num_true'] = count_model_num_true
    result['count_model_num_false'] = count_model_num_false
    result['length_gold'] = length_gold
    result['length_model'] = length_model
    result['set_isEmpty'] = len(gold_value_set) == 0

    return result


def main():
    file_output = './output.txt'
    file_output_toLong = './output_toLong.txt'
    file_output_error = './output_error.txt'

    # with open(file_output, 'a', encoding='utf-8') as file:
    #     # 将标准输出重定向到文件
    #     sys.stdout = file
    #     print("----------start-------------------")

    # 恢复标准输出
    sys.stdout = sys.__stdout__
    print("----------start-------------------")

    file_result_all = './SpCQL_all_Neo4j_data/SpCQL_all_Neo4j_data_V2.json'

    datas = read_large_json_to_list(file_result_all)

    result_set_isEmpty = 0

    for data in datas:
        # print(data)

        gold_answer = data['answer']
        model_answer = data['result-neo4j-answer']

        # print(gold_answer)
        # print(model_answer)

        # if gold_answer == "[{'p': '(东冲西撞)-[:Tag {}]->(字词)<-[:Tag {}]-(东冲西突)'}]":
        #     print(data)
        #     result_set_isEmpty += 1
        #     continue
        #
        # if model_answer == "[{'p': Node('ENTITY', name='24小时')}]":
        #     print(data)
        #     result_set_isEmpty += 1
        #     continue
        #
        # gold_answer = ast.literal_eval(gold_answer)
        #
        # model_answer = ast.literal_eval(model_answer)

        # print(data['answer'])
        # print(data['result-neo4j-answer'])

        result = count_true(gold_answer, model_answer)

        # print(result)

        if result['set_isEmpty']:
            result_set_isEmpty += 1

    print(result_set_isEmpty / len(datas))




    # 恢复标准输出
    sys.stdout = sys.__stdout__
    print("\n----------end-------------------")



if __name__ == "__main__":
    print("\nstart:\n\n")
    main()
    print("\n\nend!!!\n\n")



