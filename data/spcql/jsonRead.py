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

    # large_data = read_large_json(file_path)
    data_dev = load_json(file_dev_path)
    # data_test = load_json(file_test_path)
    # data_train = load_json(file_train_path)

    for data in data_dev:
        print(data['query'], end="  -->  ")
        print(data['cypher'], end="  -->  ")
        print(data['answer'], end="  -->  ")
        print()

    print("----------end-------------------")

if __name__ == "__main__":
    main()
