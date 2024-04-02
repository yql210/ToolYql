import json
import sys

def is_logical_equivalent(query1, query2):
    """
    一个简单的函数来判断两个CQL查询是否逻辑等价。
    这里我们假设query1和query2是两个字符串形式的CQL查询。
    在实际应用中，这个函数可能需要解析CQL查询并比较它们的抽象语法树（AST）。
    """
    # 这里我们简化处理，假设两个查询字符串相等就意味着逻辑等价
    # 实际上，你需要一个更复杂的解析和比较逻辑
    return query1 == query2

def logical_accuracy(model_queries, gold_queries):
    """
    计算模型生成的CQL查询与黄金标准查询的逻辑准确度。
    model_queries: 模型生成的查询列表
    gold_queries: 黄金标准的查询列表
    """
    # 确保模型生成的查询和黄金标准查询的数量相同
    assert len(model_queries) == len(gold_queries), "The number of model and gold queries must be the same."

    # 初始化逻辑等价的计数器
    logical_matches = 0

    # 比较每个模型生成的查询与对应的黄金标准查询
    for model_query, gold_query in zip(model_queries, gold_queries):
        if is_logical_equivalent(model_query['conversations'][1]['value'], gold_query['Output']):
            logical_matches += 1
        # else:
        #     print(model_query['conversations'][1]['value'])
        #     print(gold_query['Output'])
        #     print()

    # 计算逻辑准确度
    accuracy = logical_matches / len(model_queries)

    print("正确的个数： " + str(logical_matches))
    print("全部测试数据的个数： " + str(len(model_queries)))
    print("正确率： " + str(accuracy))

    return accuracy


def read_large_json_to_list(file_path):
    data_list = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            data_list.append(json.loads(line))
    return data_list


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
    file_output = 'DataFromGlm4ToSelfRAG/save_all/output.txt'
    file_output_toLong = 'DataFromGlm4ToSelfRAG/save_all/output_toLong.txt'
    file_output_error = 'DataFromGlm4ToSelfRAG/save_all/output_error.txt'

    # with open(file_output, 'a', encoding='utf-8') as file:
    #     # 将标准输出重定向到文件
    #     sys.stdout = file
    #     print("----------start-------------------")

    # 恢复标准输出
    sys.stdout = sys.__stdout__
    print("----------start-------------------")

    file_original_no_prompt = './SpCQL_Cypher_To_Finetun/test_cypher_tran_no_prompt.json'

    # file_original_prompt = './SpCQL_Cypher_To_Finetun/test_cypher_tran_prompt.json'
    # file_result_prompt = './result/test_cypher_tran_prompt_result.json'



    # file_result_no_prompt = './result/test_cypher_tran_no_prompt_result.json'

    file_result_no_prompt = './result/test_cypher_tran_no_prompt_result_chatglm3_epoch150.json'

    file_result_no_prompt = './result/test_cypher_tran_no_prompt_result_chatglm3_epoch4.json'

    file_result_no_prompt = './result/test_cypher_tran_no_prompt_result_baichuan2_13b_epoch40.json'

    file_result_no_prompt = './result/test_cypher_tran_no_prompt_result_baichuan2_13b_epoch150.json'

    # file_result_no_prompt = './result/test_cypher_tran_no_prompt_result_chatglm3_epoch6.json'
    #
    # file_result_no_prompt = './result/test_cypher_tran_no_prompt_result_chatglm3_epoch10.json'

    # file_result_no_prompt = './result/test_cypher_tran_no_prompt_result_baichuan2_13b_epoch4.json'

    # file_result_no_prompt = './result/test_cypher_tran_no_prompt_result_baichuan2_13b_epoch6.json'

    file_result_no_prompt = './result/test_cypher_tran_no_prompt_result_baichuan2_13b_epoch10.json'
    #



    datas_original = read_large_json_to_list(file_original_no_prompt)
    datas_result = read_large_json_to_list(file_result_no_prompt)

    # datas_original = read_large_json_to_list(file_original_prompt)
    # datas_result = read_large_json_to_list(file_result_prompt)

    result = logical_accuracy(datas_original, datas_result)

    # if len(datas_result) != len(datas_original):
    #     print("-----------ERROR----------------")
    #     sys.exit(400)
    #
    # for data_original, data_result in zip(datas_original, datas_result):
    #     print(data_original)
    #     print(data_result)
    print(result)


    print("--------------end----------------")














if __name__ == "__main__":
    main()
