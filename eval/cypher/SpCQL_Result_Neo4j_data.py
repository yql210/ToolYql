import json
import sys
import time
import func_timeout
from func_timeout import func_set_timeout
from threading import Thread
from py2neo import Graph, NodeMatcher, RelationshipMatcher
import jsonlines

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


@func_set_timeout(30)
def get_result_from_neo4j(query):
    return graph.run(query).data()


def main():
    file_output = './output.txt'
    file_output_toLong = './output_toLong.txt'
    file_output_error = './output_error.txt'
    file_output_timeout = './output_timeout.txt'

    # with open(file_output, 'a', encoding='utf-8') as file:
    #     # 将标准输出重定向到文件
    #     sys.stdout = file
    #     print("----------start-------------------")

    # 恢复标准输出
    sys.stdout = sys.__stdout__
    print("----------start-------------------")

    file_original_no_prompt = './SpCQL_Cypher_To_Finetun/test_cypher_tran_no_prompt.json'
    file_result_no_prompt = './result/test_cypher_tran_no_prompt_result.json'

    file_original_prompt = './SpCQL_Cypher_To_Finetun/test_cypher_tran_prompt.json'
    file_result_prompt = './result/test_cypher_tran_prompt_result.json'

    file_spcql_all = './SpCQL_all/SpCQL_test_train_V2.jsonl'
    file_spcql_all_neo4j_data = './SpCQL_all_Neo4j_data/SpCQL_all_Neo4j_data.json'

    data_spcql_all = load_jsonlines(file_spcql_all)

    datas_original = read_large_json_to_list(file_original_no_prompt)
    datas_result = read_large_json_to_list(file_result_no_prompt)

    # datas_original = read_large_json_to_list(file_original_prompt)
    # datas_result = read_large_json_to_list(file_result_prompt)

    file_save_path = file_spcql_all_neo4j_data

    connect_true = 0
    connect_false = 0
    connect_false_timeout = 0
    index_count = 0
    connect_list_isEmpty = 0

    counect_flag_timeout = False
    counect_flag_error = False


    index = 0
    index1 = 0
    id_index = 0
    items = []
    length = int(len(data_spcql_all) / 10) * 10

    # for data_result in datas_result:
    for i in range(0, len(data_spcql_all)):
        # index_count += 1
        #
        # if index_count == 2001:
        #     break

        print(i)
        print(datas_result[i]['Input'])
        print(datas_result[i]['Output'])
        print()

        counect_flag_timeout = False
        counect_flag_error = False
        result = []

        try:
            # result = []
            # result = graph.run(datas_result[i]['Output']).data()
            result = get_result_from_neo4j(datas_result[i]['Output'])
            if result is not None:
                connect_true += 1
            if len(result) == 0:
                connect_list_isEmpty += 1
        except func_timeout.exceptions.FunctionTimedOut:
            print("Function execution has timed out.")
            counect_flag_timeout = True
            connect_false_timeout += 1
            print("---------------------error-------------------------------")
            print(datas_result[i]['Input'])
            print(datas_result[i]['Output'])
            print()
            with open(file_output_timeout, 'a', encoding='utf-8') as file:
                # 将标准输出重定向到文件
                sys.stdout = file
                print("Function execution has timed out.")
                print(i)
                print(datas_result[i])
                print(datas_result[i]['Input'])
                print(datas_result[i]['Output'])
                print()

            # 恢复标准输出
            sys.stdout = sys.__stdout__

            time.sleep(10)
        except Exception as e:
            # 如果发生了其他类型的异常，执行这里的代码
            print("An error occurred:", e)
            connect_false += 1
            counect_flag_error = True
            print()
            print("---------------------error-------------------------------")
            print(datas_result[i]['Input'])
            print(datas_result[i]['Output'])
            print()
            with open(file_output_error, 'a', encoding='utf-8') as file:
                # 将标准输出重定向到文件
                sys.stdout = file
                print("An error occurred:", e)
                print(i)
                print(datas_result[i])
                print(datas_result[i]['Input'])
                print(datas_result[i]['Output'])
                print()

            # 恢复标准输出
            sys.stdout = sys.__stdout__
            time.sleep(10)

        if data_spcql_all[i]['instruction'] != datas_result[i]['Input']:
            raise ValueError("值错误，发生了一些不正确的事情")

        conversation = {"instruction": data_spcql_all[i]['instruction'],
                        "cypher": data_spcql_all[i]['cypher'],
                        "answer": str(data_spcql_all[i]['answer']),
                        "glm-4-answer": data_spcql_all[i]['glm-4-answer'],
                        "selfRAG-answer": data_spcql_all[i]['output'],
                        "result-cypher": datas_result[i]['Output'],
                        "result-neo4j-answer": str(result),
                        "result-neo4j-error": counect_flag_error,
                        "result-neo4j-timeout": counect_flag_timeout,
                        "input": data_spcql_all[i]['input'],
                        "topic": data_spcql_all[i]['topic'],
                        "id": data_spcql_all[i]['id'],
                        "dataset_name": "SpCQL_test"}

        conversation = json.dumps(conversation, ensure_ascii=False)
        items.append(conversation)
        # print(conversation)
        index += 1

        if index == 50:
            store_json_per_line(items, file_save_path)
            index = 0
            items = []
            with open(file_output, 'a', encoding='utf-8') as file:
                # 将标准输出重定向到文件
                sys.stdout = file
                print("--------------" + str(index1) + "----------------")
            # 恢复标准输出
            sys.stdout = sys.__stdout__

    store_json_per_line(items, file_save_path)
    with open(file_output, 'a', encoding='utf-8') as file:
        # 将标准输出重定向到文件
        sys.stdout = file
        print("--------------" + str(index1) + "----------------")
        print(index1)
        print("\n----------end-------------------")
    # 恢复标准输出
    sys.stdout = sys.__stdout__

    print("Connect success:", connect_true)
    print("Connect list is empty:", connect_list_isEmpty)
    print("Connect false:", connect_false)
    print("Connect false timeout:", connect_false_timeout)
    print("connect all:", len(data_spcql_all))
    print("acc: ", connect_true/len(data_spcql_all))
    print("--------------end----------------")














if __name__ == "__main__":
    graph = Graph("http://172.16.44.106:7474", auth=("neo4j", "neo4jneo4j"))

    main()
