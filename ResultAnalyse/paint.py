import json

def read_large_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            yield json.loads(line)



def main():


    file_path = "./1113-pt/trainer_state.json"
    output_file = "./data/change/valid_en.jsonl"



    # 创建一个生成器，逐行读取 JSON 文件
    large_data = read_large_json(file_path)

    index = 0
    index1 = 0
    items = []
    # 在这里处理每个 JSON 对象
    for item in large_data:
        print(item["epoch"])


    print(index1)

if __name__ == "__main__":
    main()
