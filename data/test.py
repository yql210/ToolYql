import json

def generate_conversation_json():

    conversation = {
        "conversations": [
            {"from": "human", "value": "问题"},
            {"from": "gpt", "value": "回复"},
        ],
    }

    # 将对话列表转换为 JSON 对象
    json_data = json.dumps(conversation)

    # 拼接 JSON 对象，生成最终 JSON 字符串
    # final_json = "[" + ",".join(json_data) + "]"

    return json_data

if __name__ == "__main__":
    json_string = generate_conversation_json()
    print(json_string)
