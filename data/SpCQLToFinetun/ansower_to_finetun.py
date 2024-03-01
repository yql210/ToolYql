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
    file_output = 'SpCQLFromGlm4/output.txt'
    file_output_toLong = 'SpCQLFromGlm4/output_toLong.txt'
    file_output_error = 'SpCQLFromGlm4/output_error.txt'

    with open(file_output, 'a', encoding='utf-8') as file:
        # 将标准输出重定向到文件
        sys.stdout = file
        print("----------start-------------------")

    # 恢复标准输出
    sys.stdout = sys.__stdout__
    print("----------start-------------------")

    file_dev_path = './SpCQLFromGlm4/dev_save_V1.json'
    file_test_path = './SpCQLFromGlm4/test_save_V1.json'
    file_train_path = './SpCQLFromGlm4/train_save_V1.json'

    file_dev_save_path_prompt = './SpCQLFromGlm4/dev_filt_tran_prompt.json'
    file_test_save_path_prompt = './SpCQLFromGlm4/test_filt_tran_prompt.json'
    file_train_save_path_prompt = './SpCQLFromGlm4/train_filt_tran_prompt.json'

    file_dev_save_path_no_prompt = './SpCQLFromGlm4/dev_filt_tran_no_prompt.json'
    file_test_save_path_no_prompt = './SpCQLFromGlm4/test_filt_tran_no_prompt.json'
    file_train_save_path_no_prompt = './SpCQLFromGlm4/train_filt_tran_no_prompt.json'

    file_dev_save_path_no_prompt_no_kg = './SpCQLFromGlm4/dev_filt_tran_no_prompt_no_kg.json'
    file_test_save_path_no_prompt_no_kg = './SpCQLFromGlm4/test_filt_tran_no_prompt_no_kg.json'
    file_train_save_path_no_prompt_no_kg = './SpCQLFromGlm4/train_filt_tran_no_prompt_no_kg.json'

    # datas = read_large_json(file_dev_path)
    # datas = read_large_json(file_test_path)
    datas = read_large_json(file_train_path)

    file_save_path = file_train_save_path_no_prompt_no_kg

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

        # message = ("作为可以根据问题和知识库的信息完美的生成可以通过图灵测试回答的知识库检索型对话专家，回答的受众是对知识库信息出现在回答中要求很高，并且回答精炼。提供的回答高度契合知识库信息，语言流畅，无关信息不要回复。在回答时，请扮演一个儒雅的老者，根据知识库中的信息给出确切回复，回复一段或者一句话。"
        #                    "\n问题：" + data['query'] +
        #                    "\n知识：" + str(data['answer'])
        #            )

        # message = ("问题：" + data['query'] +
        #                    "\n知识：" + str(data['answer'])
        #            )

        message = data['query']

        conversation = {
                    "conversations":
                        [
                            {
                                "from": "human",
                                "value": message
                            },
                            {
                                "from": "gpt",
                                "value": data['glm-4-answer']
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
