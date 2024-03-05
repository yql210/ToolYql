import json

input_path = "./DataFromGlm4ToSelfRAG/SpCQL_dev_SelfRAG_V1_save/SpCQL_dev_SelfRAG_V1_save.json"

op = open(input_path)

input_data = json.load(op)

print("end")
