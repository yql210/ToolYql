import json
import sys
import jsonlines
from tqdm import tqdm


def read_large_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            yield json.loads(line)


def store_json_per_line(json_data, output_file):
    with open(output_file, "a", encoding="utf-8") as file:
        for item in json_data:
            # json.dump(item, file, ensure_ascii=False, indent=4)
            file.write(item + "\n")


def load_jsonlines(file):
    with jsonlines.open(file, 'r') as jsonl_f:
        lst = [obj for obj in jsonl_f]
    return lst


def load_json(fname, mode="r", encoding="utf8"):
    if "b" in mode:
        encoding = None
    with open(fname, mode=mode, encoding=encoding) as f:
        return json.load(f)

def load_file(file_name):
    print(file_name)
    if file_name.endswith(".json"):
        data = json.load(open(file_name, encoding="utf-8"))
    elif file_name.endswith(".jsonl"):
        data = load_jsonlines(file_name)
    else:
        if ".json_" in file_name:
            data = json.load(open(file_name))
        elif ".jsonl_" in file_name:
            data = load_jsonlines(file_name)
    return data


def load_all_files(file_paths):
    final_results = {}
    # for fp in file_paths:
    data = load_file(file_paths)
    for item in data:
        q_id = item["id"] if "id" in item else item["q_id"]
        final_results.setdefault(q_id, [])
        final_results[q_id].append(item)
    return final_results


def count_true(answer, output):
    """
    统计gold_answer与model_answer之间进行对比的相关数据
    :param gold_answer: 最原始的数据，即标准数据
    :param model_answer:  模型产生的数据，即生成数据
    :return: {'count_gold_num': 3, 'count_model_num': 4, 'count_model_num_true': 3, 'count_model_num_false': 1,
                'length_gold': 3, 'length_model': 3, 'set_isEmpty': True}
    """
    count_num = 0
    count_num_num = 0
    # count_model_num_true = 0
    # count_model_num_false = 0

    result = '[No support / Contradictory]'

    # # 创建一个空集合用于存储唯一的value键
    # gold_value_set = set()

    for dict_answer in answer:
        # 假设每个字典只有一个键值对
        for key, value in dict_answer.items():
            try:
                if str(value) in output:
                    count_num_num += 1
                count_num += 1
            except Exception as e:
                print(e)

    if count_num_num > 0:
        result = '[Partially supported]'

    if count_num == count_num_num:
        result = '[Fully supported]'

    if count_num == 0:
        result = '[Fully supported]'

    return result


def main():
    file_output = './FINAL_OUTPUT_PATH/output.txt'
    file_output_toLong = './FINAL_OUTPUT_PATH/output_toLong.txt'
    file_output_error = './FINAL_OUTPUT_PATH/output_error.txt'

    # with open(file_output, 'a', encoding='utf-8') as file:
    #     # 将标准输出重定向到文件
    #     sys.stdout = file
    #     print("----------start-------------------")
    #
    # # 恢复标准输出
    # sys.stdout = sys.__stdout__
    # print("----------start-------------------")

    # file_path = './sa-self-gen-data-after-retrieval/0405_sa_rag_1.3b_epcoh_20_after_retrieval.jsonl'
    # file_path = './sa-self-gen-data-after-retrieval/0405_sa_rag_1.3b_epcoh_5_after_retrieval.jsonl'
    # file_path = './sa-self-gen-data-after-retrieval/0405_sa_rag_1.3b_epcoh_10_after_retrieval.jsonl'
    file_path = './sa-self-gen-data-after-retrieval/0405_sa_rag_1.3b_epcoh_3_after_retrieval.jsonl'


    # input_test_datas = load_file(file_test_path)
    input_datas = load_file(file_path)


    FF = 0
    FP = 0
    FN = 0
    F_num = 0

    PF = 0
    PP = 0
    PN = 0
    P_num = 0

    NF = 0
    NP = 0
    NN = 0
    N_num = 0




    for data in input_datas:
        # print(data)
        if data['Retrieval'] == "[Retrieval]":
            answer = data['answer']
            answer = eval(answer)
            output = data['SA_RAG_data'][0]
            isSup = data['isSup']   # 原始数据中的最原始结果
            result_isSup = count_true(answer, output)  # 生成的回复和检索到的answer进行对比

            if isSup == '[Fully supported]':
                if result_isSup == '[Fully supported]':
                    FF += 1
                elif result_isSup == '[Partially supported]':
                    FP += 1
                elif result_isSup == '[No support / Contradictory]':
                    FN += 1
                else:
                    F_num += 1

            elif isSup == '[Partially supported]':
                if result_isSup == '[Fully supported]':
                    PF += 1
                elif result_isSup == '[Partially supported]':
                    PP += 1
                elif result_isSup == '[No support / Contradictory]':
                    PN += 1
                else:
                    P_num += 1

            elif isSup == '[No support / Contradictory]':
                if result_isSup == '[Fully supported]':
                    NF += 1
                elif result_isSup == '[Partially supported]':
                    NP += 1
                elif result_isSup == '[No support / Contradictory]':
                    NN += 1
                else:
                    N_num += 1


    print()
    print("          Fully    Partially        No    error")
    print("Fully      " + str(FF) + "          " + str(PF) + "          " + str(NF) + "    " + str(F_num))
    print("Partially  " + str(FP) + "          " + str(PP) + "          " + str(NP) + "    " + str(P_num))
    print("No         " + str(FN) + "          " + str(PN) + "          " + str(NN) + "    " + str(N_num))



if __name__ == "__main__":
    print("\nstart:\n\n")
    main()
    print("\n\nend!!!\n\n")





