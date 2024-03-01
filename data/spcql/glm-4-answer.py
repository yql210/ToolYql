from zhipuai import ZhipuAI
import json
import sys
import time



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
    with open('SpCQL/output.txt', 'a', encoding='utf-8') as file:
        # 将标准输出重定向到文件
        sys.stdout = file
        print("----------start-------------------")

    client = ZhipuAI(api_key="2178e91663c1f74a6f61b53eef5abd82.4sk2Una0UGk3nODJ")

    # file_dev_path = './SpCQL/dev.json'
    file_test_path = './SpCQL/test.json'
    # file_train_path = './SpCQL/train.json'

    # file_dev_save_path = './SpCQL/dev_save.json'
    file_test_save_path = './SpCQL/test_save.json'
    # file_train_save_path = './SpCQL/train_save.json'

    # large_data = read_large_json(file_path)
    # datas = load_json(file_dev_path)
    # datas = load_json(file_test_path)
    datas = load_json(file_test_path)

    index = 0
    index1 = 0
    items = []

    for data in datas:

        # if index1 == 15:
        #     break

        if index1 < 1400:
            index1 += 1
            continue

        if len(data['answer']) > 10240:
            # 恢复标准输出
            sys.stdout = sys.__stdout__
            print(f"{index1} --------data['answer'] 过长，放弃治疗---------长度为{len(data['answer'])}------------")
            print()
            print()
            print()
            with open('SpCQL/output_toLong.txt', 'a', encoding='utf-8') as file:
                # 将标准输出重定向到文件
                sys.stdout = file
                print(f"{index1} --------data['answer'] 过长，放弃治疗---------------------")
                print()
            continue

        message = [
            {
                "role": "user",
                "content": "作为可以根据问题和知识库的信息完美的生成可以通过图灵测试回答的知识库检索型对话专家，回答的受众是对知识库信息出现在回答中要求很高，并且回答精炼。提供的回答高度契合知识库信息，语言流畅，无关信息不要回复。在回答时，请扮演一个儒雅的老者，根据知识库中的信息给出确切回复，回复一段或者一句话。"
                           "\n问题：" + data['query'] +
                           "\n知识：" + str(data['answer'])
            }
        ]

        with open('SpCQL/output.txt', 'a', encoding='utf-8') as file:
            # 将标准输出重定向到文件
            sys.stdout = file
            print()
            print(index1)
            print("问题：" + data['query'] + "\n知识：" + str(data['answer']))

        # 恢复标准输出
        sys.stdout = sys.__stdout__
        print()
        print(index1)
        print("问题：" + data['query'] + "\n知识：" + str(data['answer']))

        response_str = ""

        try:
            # 可能引发异常的代码
            response = client.chat.completions.create(
                model="glm-4",
                messages=message,
                top_p=0.7,
                temperature=0.95,
                max_tokens=1024,
                stream=True,
            )
        except Exception as e:
            # 处理异常
            sys.stdout = sys.__stdout__
            print(f"An error occurred: {e}")
            print(f"{index1} --------An error occurred------------")
            print()
            with open('SpCQL/output_error.txt', 'a', encoding='utf-8') as file:
                # 将标准输出重定向到文件
                sys.stdout = file
                print(f"An error occurred: {e}")
                print(f"{index1} --------An error occurred------------")
                print()
            time.sleep(60)  # 延迟60秒
            response_str = "ERROR"

        # 恢复标准输出
        sys.stdout = sys.__stdout__

        for trunk in response:
            print(trunk.choices[0].delta.content, end="")
            response_str += trunk.choices[0].delta.content

        print()

        with open('SpCQL/output.txt', 'a', encoding='utf-8') as file:
            # 将标准输出重定向到文件
            sys.stdout = file
            print(response_str)

        data['glm-4-answer'] = response_str

        data = json.dumps(data, ensure_ascii=False)
        items.append(data)

        index += 1
        index1 += 1

        if index == 10:
            store_json_per_line(items, file_test_save_path)
            index = 0
            items = []
            with open('SpCQL/output.txt', 'a', encoding='utf-8') as file:
                # 将标准输出重定向到文件
                sys.stdout = file
                print("--------------" + str(index1) + "----------------")

    store_json_per_line(items, file_test_save_path)
    with open('SpCQL/output.txt', 'a', encoding='utf-8') as file:
        # 将标准输出重定向到文件
        sys.stdout = file
        print("--------------" + str(index1) + "----------------")
        print(index1)
        print("\n----------end-------------------")

    # 恢复标准输出
    sys.stdout = sys.__stdout__


if __name__ == "__main__":
    main()
