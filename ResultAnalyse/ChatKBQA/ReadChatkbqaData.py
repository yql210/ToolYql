import json

def read_json_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data

# 请将下面的文件路径替换为你的JSON文件路径
# json_file_path = 'E:\\tem\chatkbqa\\240106\data\\WebQSP_Freebase_NQ_test\\examples.json'
json_file_path = 'E:\\tem\\chatkbqa\\240106\\data\\WebQSP_Freebase_NQ_test\\examples_split.json'

json_data = read_json_file(json_file_path)



print("end")