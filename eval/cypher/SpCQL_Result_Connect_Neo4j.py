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


@func_set_timeout(3)
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

    data_spcql_all = load_jsonlines(file_spcql_all)

    datas_original = read_large_json_to_list(file_original_no_prompt)
    datas_result = read_large_json_to_list(file_result_no_prompt)

    # datas_original = read_large_json_to_list(file_original_prompt)
    # datas_result = read_large_json_to_list(file_result_prompt)

    # 连接到Neo4j数据库
    # 创建一个包含超时设置的配置字典
    config = {
        "timeout": 10  # 设置超时时间为10秒
    }


    connect_true = 0
    connect_false = 0
    connect_false_timeout = 0
    index_count = 0

    for data_result in datas_result:
        index_count += 1

        print(index_count)
        print(data_result['Input'])
        print(data_result['Output'])
        print()

        # if data_result['Output'] == "match (:ENTITY{name:'生活节目'})<-[*]-(m), (m)-[:Relationship{name:'播出电视'}]->(n) return m.name,n.name limit 3":
        #     continue
        # if data_result['Output'] == "match (n:ENTITY{name:'巴法络PNT500U3B'})-[*]->(x) where x.name<>'需要巴法络PNT500U3B' return distinct x.name":
        #     continue
        # if data_result['Output'] == "match (:ENTITY{name:'豆腐'})<-[:Relationship*]-(m), (m)-[:Relationship{name:'辅料'}]->(n) return distinct m.name,n.name limit 3":
        #     continue
        # if data_result['Output'] == "match (:ENTITY{name:'甜品'})<-[*]-(m), (m)-[:Relationship{name:'主要食材'}]->(n) return m.name,n.name limit 10":
        #     continue
        # if data_result['Output'] == "match (:ENTITY{name:'酒店'})<-[:Relationship*]-(m), (m)-[:Relationship{name:'地址'}]->(n) return m.name,n.name limit 6":
        #     continue
        # if data_result['Output'] == "match (:ENTITY{name:'车站'})<-[*]-(m), (m)-[:Relationship{name:'站台数'}]->(n) return m.name,n.name limit 6":
        #     continue


        try:
            # result = graph.run(data_result['Output']).data()
            result = get_result_from_neo4j(data_result['Output'])
            if result is not None:
                connect_true += 1
        except func_timeout.exceptions.FunctionTimedOut:
            print("Function execution has timed out.")

            connect_false_timeout += 1
            print("---------------------error-------------------------------")
            print(data_result['Input'])
            print(data_result['Output'])
            print()
            with open(file_output_timeout, 'a', encoding='utf-8') as file:
                # 将标准输出重定向到文件
                sys.stdout = file
                print("Function execution has timed out.")
                print(index_count)
                print(data_result)
                print(data_result['Input'])
                print(data_result['Output'])
                print()

            # 恢复标准输出
            sys.stdout = sys.__stdout__

            time.sleep(10)
        except Exception as e:
            # 如果发生了其他类型的异常，执行这里的代码
            print("An error occurred:", e)
            connect_false += 1

            print()
            print("---------------------error-------------------------------")
            print(data_result['Input'])
            print(data_result['Output'])
            print()
            with open(file_output_error, 'a', encoding='utf-8') as file:
                # 将标准输出重定向到文件
                sys.stdout = file
                print("An error occurred:", e)
                print(index_count)
                print(data_result)
                print(data_result['Input'])
                print(data_result['Output'])
                print()

            # 恢复标准输出
            sys.stdout = sys.__stdout__
            time.sleep(10)


    print("Connect success:", connect_true)
    print("Connect false:", connect_false)
    print("Connect false timeout:", connect_false_timeout)
    print("connect all:", index_count)
    print("acc: ", connect_true/index_count)
    print("--------------end----------------")














if __name__ == "__main__":
    graph = Graph("http://172.16.44.106:7474", auth=("neo4j", "neo4jneo4j"))

    main()
