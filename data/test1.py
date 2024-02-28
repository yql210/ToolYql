import json
import os

# input_file = "large_input.json"  # 替换为您的超大 JSON 文件路径
output_file_prefix = "small_output_"  # 替换为您希望保存的文件前缀
input_file = "./data/test_zh_0.json"
output_file = "./data/change_test_zh.json"

def read_large_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def save_batch_json(data, output_prefix):
    batch_size = 100  # 修改为适合您的批次大小
    count = 0

    while data:
        batch_data = data[:batch_size]
        data = data[batch_size:]

        with open(f"{output_prefix}_{count}.json", "w", encoding="utf-8") as file:
            json.dump(batch_data, file, ensure_ascii=False, indent=4)

        count += 1

def main():
    data = read_large_json(input_file)
    save_batch_json(data, output_file_prefix)

if __name__ == "__main__":
    main()
