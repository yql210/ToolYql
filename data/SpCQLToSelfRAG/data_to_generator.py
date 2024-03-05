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
    file_output = 'DataFromGlm4ToSelfRAG/output.txt'
    file_output_toLong = 'DataFromGlm4ToSelfRAG/output_toLong.txt'
    file_output_error = 'DataFromGlm4ToSelfRAG/output_error.txt'

    with open(file_output, 'a', encoding='utf-8') as file:
        # 将标准输出重定向到文件
        sys.stdout = file
        print("----------start-------------------")

    # 恢复标准输出
    sys.stdout = sys.__stdout__
    print("----------start-------------------")

    file_train_path_test = './DataFromGlm4ToSelfRAG/yuanql_file_test.json'
    file_dev_path = './DataFromGlm4ToSelfRAG/dev_save_V1.json'
    file_test_path = './DataFromGlm4ToSelfRAG/test_save_V1.json'
    file_train_path = './DataFromGlm4ToSelfRAG/train_save_V1.json'

    file_dev_save_path = './DataFromGlm4ToSelfRAG/SpCQL_dev_SelfRAG_V1_save.json'
    file_test_save_path = './DataFromGlm4ToSelfRAG/SpCQL_test_SelfRAG_V1_save.json'
    file_train_save_path = './DataFromGlm4ToSelfRAG/SpCQL_train_SelfRAG_V1_save.json'

    # datas = read_large_json(file_train_path_test)
    # datas = read_large_json(file_dev_path)
    # datas = read_large_json(file_test_path)
    datas = read_large_json(file_train_path)

    # file_save_path = file_dev_save_path
    # file_save_path = file_test_save_path
    file_save_path = file_train_save_path

    index = 0
    index1 = 0
    id_index = 0
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

        message = ("一个好奇的用户和一个人工智能助手之间的聊天。\n助手会对用户的问题给出有用的、详细的、礼貌的回答。"
                           "\n问题：" + data['query']
                   )

        conversation = {"instruction": message,
                        "output": data['glm-4-answer'],
                        "input": "",
                        "topic": "",
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


if __name__ == "__main__":
    main()
