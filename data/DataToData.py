import json

def read_large_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            yield json.loads(line)


def store_json_per_line(json_data, output_file):
    with open(output_file, "a", encoding="utf-8") as file:
        for item in json_data:
            # json.dump(item, file, ensure_ascii=False, indent=4)
            file.write(item + "\n")



def main():
    # file_path = "./data/test_zh_0.json"
    # output_file = "./data/change/test_zh.jsonl"

    # file_path = "./data/train_zh_0.json"
    # output_file = "./data/change/train_zh.jsonl"

    # file_path = "./data/valid_zh_0.json"
    # output_file = "./data/change/valid_zh.jsonl"


# # --------------英文-----------------------
#     file_path = "./data/test_en_1.json"
#     output_file = "./data/change/test_en.jsonl"

    # file_path = "./data/train_en_1.json"
    # output_file = "./data/change/train_en.jsonl"

    file_path = "./data/valid_en_1.json"
    output_file = "./data/change/valid_en.jsonl"



    # 创建一个生成器，逐行读取 JSON 文件
    large_data = read_large_json(file_path)

    index = 0
    index1 = 0
    items = []
    # 在这里处理每个 JSON 对象
    for item in large_data:

        # conversation = {"conversations": [{"from": "human", "value": item["instruction"]}, {"from": "gpt", "value": item["output"]}]}
        conversation = {"conversations": [{"from": "human", "value": item["input"]}, {"from": "gpt", "value": item["output"]}]}

        conversation = json.dumps(conversation, ensure_ascii=False)
        items.append(conversation)
        # print(conversation)
        index += 1
        index1 += 1
        if index == 5000:
            store_json_per_line(items, output_file)
            index = 0
            items = []
            print("--------------" + str(index1) + "----------------")

    store_json_per_line(items, output_file)
    print("--------------" + str(index1) + "----------------")
    print(index1)

if __name__ == "__main__":
    main()
