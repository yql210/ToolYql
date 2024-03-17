import json
import sys
from py2neo import Graph, NodeMatcher, RelationshipMatcher

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

def main():

    file_output = 'DataFromGlm4ToSelfRAG/save_all/output.txt'
    file_output_toLong = 'DataFromGlm4ToSelfRAG/save_all/output_toLong.txt'
    file_output_error = 'DataFromGlm4ToSelfRAG/save_all/output_error.txt'

    # with open(file_output, 'a', encoding='utf-8') as file:
    #     # 将标准输出重定向到文件
    #     sys.stdout = file
    #     print("----------start-------------------")

    # 恢复标准输出
    sys.stdout = sys.__stdout__
    print("----------start-------------------")

    # 连接到Neo4j数据库
    graph = Graph("http://172.16.44.106:7474", auth=("neo4j", "neo4jneo4j"))

    # 执行Cypher查询
    result = graph.run(
        "match (n:ENTITY{name:'九年级物理/北大绿卡'})-[:Relationship*1..2]->(x) where x.name<>'出版物' return distinct x.name").data()
    for record in result:
        print(record)



    print("111")














if __name__ == "__main__":
    main()





