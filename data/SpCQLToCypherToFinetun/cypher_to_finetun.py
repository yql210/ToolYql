import json
import sys


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
    file_output = 'CypherToFinetun/output.txt'
    file_output_toLong = 'CypherToFinetun/output_toLong.txt'
    file_output_error = 'CypherToFinetun/output_error.txt'

    with open(file_output, 'a', encoding='utf-8') as file:
        # 将标准输出重定向到文件
        sys.stdout = file
        print("----------start-------------------")

    # 恢复标准输出
    sys.stdout = sys.__stdout__
    print("----------start-------------------")

    file_dev_path = './CypherToFinetun/dev_save_V1.json'
    file_test_path = './CypherToFinetun/test_save_V1.json'
    file_train_path = './CypherToFinetun/train_save_V1.json'

    file_dev_save_path_prompt = './CypherToFinetun/dev_cypher_tran_prompt.json'
    file_test_save_path_prompt = './CypherToFinetun/test_cypher_tran_prompt.json'
    file_train_save_path_prompt = './CypherToFinetun/train_cypher_tran_prompt.json'

    file_dev_save_path_no_prompt = './CypherToFinetun/dev_cypher_tran_no_prompt.json'
    file_test_save_path_no_prompt = './CypherToFinetun/test_cypher_tran_no_prompt.json'
    file_train_save_path_no_prompt = './CypherToFinetun/train_cypher_tran_no_prompt.json'

    # datas = read_large_json(file_dev_path)
    # datas = read_large_json(file_test_path)
    datas = read_large_json(file_train_path)

    file_save_path = file_train_save_path_prompt

    index = 0
    index1 = 0
    items = []

    for data in datas:
        index1 += 1

        # if index1 == 15:
        #     break

        # if index1 < 1400:
        #     index1 += 1
        #     continue

        # 过滤输入长度的限制,长度限制8K
        if len(data['answer']) > 8192:
            # 恢复标准输出
            sys.stdout = sys.__stdout__
            print(f"{index1} --------data['answer'] 过长，放弃治疗---------长度为:{len(data['answer'])}------------")
            print()
            print()
            print()
            with open(file_output_toLong, 'a', encoding='utf-8') as file:
                # 将标准输出重定向到文件
                sys.stdout = file
                print(f"{index1} --------data['answer'] 过长，放弃治疗---------长度为:{len(data['answer'])}------------")
                print()
            continue

        # 回复为ERROR的限制或者为空的限制
        if data['glm-4-answer'] == "ERROR" or data['glm-4-answer'] == "":
            # 恢复标准输出
            sys.stdout = sys.__stdout__
            print(f"{index1} --------回复为ERROR的限制或者为空的限制---------长度为{len(data['answer'])}------------")
            print("问题：" + data['query'] + "\n知识：" + str(data['answer']) + "\n回复:" + data['glm-4-answer'])
            print()
            print()
            with open(file_output_error, 'a', encoding='utf-8') as file:
                # 将标准输出重定向到文件
                sys.stdout = file
                print(f"{index1} --------回复为ERROR的限制或者为空的限制---------长度为{len(data['answer'])}------------")
                print("问题：" + data['query'] + "\n知识：" + str(data['answer']) + "\n回复:" + data['glm-4-answer'])
                print()
                print()
            continue

        message = ("作为一个优秀的neo4j数据库查询专家，可以很好理解自然语言，并根据问题生成Cypher数据库查询语句。提供的查询语句以符合cypher语句规范为前提，并尽可能的准确。在生成查询语句的时候，请扮演一个严谨的数据库查询专家，根据问题生成确切的查询语句，只回复查询语句。"
                           "\n问题：" + data['query']
                   )

        # message = data['query']

        conversation = {
                    "conversations":
                        [
                            {
                                "from": "human",
                                "value": message
                            },
                            {
                                "from": "gpt",
                                "value": data['cypher']
                            }
                        ]
                    }

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


if __name__ == "__main__":
    main()
