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

def load_json(fname, mode="r", encoding="utf8"):
    if "b" in mode:
        encoding = None
    with open(fname, mode=mode, encoding=encoding) as f:
        return json.load(f)
def main():
    print("----------start-------------------")

    file_dev_path = './SpCQL/dev.json'
    file_test_path = './SpCQL/test.json'
    file_train_path = './SpCQL/train.json'

    file_dev_save_path = './SpCQL/dev_save.json'
    file_test_save_path = './SpCQL/test_save.json'
    file_train_save_path = './SpCQL/train_save.json'

    # large_data = read_large_json(file_path)
    # data_dev = load_json(file_dev_path)
    data_test = load_json(file_test_path)
    data_train = load_json(file_train_path)

    i = 0
    index = 0
    index1 = 0
    items = []

    for data in data_train:
        # print(data['query'], end="  -->  ")
        # print(data['cypher'], end="  -->  ")
        # print(data['answer'], end="  -->  ")

        print(data['query'])
        print(data['cypher'])
        print(data['answer'])
        print()


    #     data['glm-4-answer'] = str(i)
    #     i += 1
    #
    #     data = json.dumps(data, ensure_ascii=False)
    #     items.append(data)
    #
    #     index += 1
    #     index1 += 1
    #
    #     if index == 10:
    #         break
    #
    #     if index == 5000:
    #         store_json_per_line(items, file_dev_save_path)
    #         index = 0
    #         items = []
    #         print("--------------" + str(index1) + "----------------")
    #
    # store_json_per_line(items, file_dev_save_path)
    # print("--------------" + str(index1) + "----------------")
    # print(index1)



    print("----------end-------------------")

if __name__ == "__main__":
    main()
