import json
import jsonlines
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report


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


def count_isUtility(model_answer):
    result = 'Error'

    num1 = 0
    num2 = 0
    num3 = 0
    num4 = 0
    num5 = 0

    if '[Utility:1]' in model_answer:
        num1 = 1
        result = 1
    if '[Utility:2]' in model_answer:
        num2 = 1
        result = 2
    if '[Utility:3]' in model_answer:
        num3 = 1
        result = 3
    if '[Utility:4]' in model_answer:
        num4 = 1
        result = 4
    if '[Utility:5]' in model_answer:
        num5 = 1
        result = 5

    if num1 + num2 + num3 + num4 + num5 == 1:
        return result
    else:
        return 0

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
    # file_path = './sa-self-gen-data-after-retrieval/0405_sa_rag_1.3b_epcoh_40_after_retrieval.jsonl'

    matrix_rag = np.zeros((5, 6))
    matrix_no_rag = np.zeros((5, 6))

    y_true = []
    y_pred = []

    y_true_rag = []
    y_pred_rag = []

    y_true_no_rag = []
    y_pred_no_rag = []


    input_datas = load_file(file_path)
    for data in input_datas:
        print(data)

        if data['Retrieval'] == "[Retrieval]": # 当需要进行检索的时候，走这一行

            output = data['SA_RAG_data'][0]
            isUtility = data['isUtility']
            result_isUtility = count_isUtility(output)

            if isUtility == '[Utility:1]':
                y_true_rag.append(0)
                y_true.append(0)
                if result_isUtility == 1:
                    y_pred_rag.append(0)
                    y_pred.append(0)
                    matrix_rag[0][0] += 1
                elif result_isUtility == 2:
                    y_pred_rag.append(1)
                    y_pred.append(1)
                    matrix_rag[0][1] += 1
                elif result_isUtility == 3:
                    y_pred_rag.append(2)
                    y_pred.append(2)
                    matrix_rag[0][2] += 1
                elif result_isUtility == 4:
                    y_pred_rag.append(3)
                    y_pred.append(3)
                    matrix_rag[0][3] += 1
                elif result_isUtility == 5:
                    y_pred_rag.append(4)
                    y_pred.append(4)
                    matrix_rag[0][4] += 1
                else:
                    y_pred_rag.append(5)
                    y_pred.append(5)
                    matrix_rag[0][5] += 1

            elif isUtility == '[Utility:2]':
                y_true_rag.append(1)
                y_true.append(1)
                if result_isUtility == 1:
                    y_pred_rag.append(0)
                    y_pred.append(0)
                    matrix_rag[1][0] += 1
                elif result_isUtility == 2:
                    y_pred_rag.append(1)
                    y_pred.append(1)
                    matrix_rag[1][1] += 1
                elif result_isUtility == 3:
                    y_pred_rag.append(2)
                    y_pred.append(2)
                    matrix_rag[1][2] += 1
                elif result_isUtility == 4:
                    y_pred_rag.append(3)
                    y_pred.append(3)
                    matrix_rag[1][3] += 1
                elif result_isUtility == 5:
                    y_pred_rag.append(4)
                    y_pred.append(4)
                    matrix_rag[1][4] += 1
                else:
                    y_pred_rag.append(5)
                    y_pred.append(5)
                    matrix_rag[1][5] += 1

            elif isUtility == '[Utility:3]':
                y_true_rag.append(2)
                y_true.append(2)
                if result_isUtility == 1:
                    y_pred_rag.append(0)
                    y_pred.append(0)
                    matrix_rag[2][0] += 1
                elif result_isUtility == 2:
                    y_pred_rag.append(1)
                    y_pred.append(1)
                    matrix_rag[2][1] += 1
                elif result_isUtility == 3:
                    y_pred_rag.append(2)
                    y_pred.append(2)
                    matrix_rag[2][2] += 1
                elif result_isUtility == 4:
                    y_pred_rag.append(3)
                    y_pred.append(3)
                    matrix_rag[2][3] += 1
                elif result_isUtility == 5:
                    y_pred_rag.append(4)
                    y_pred.append(4)
                    matrix_rag[2][4] += 1
                else:
                    y_pred_rag.append(5)
                    y_pred.append(5)
                    matrix_rag[2][5] += 1

            elif isUtility == '[Utility:4]':
                y_true_rag.append(3)
                y_true.append(3)
                if result_isUtility == 1:
                    y_pred_rag.append(0)
                    y_pred.append(0)
                    matrix_rag[3][0] += 1
                elif result_isUtility == 2:
                    y_pred_rag.append(1)
                    y_pred.append(1)
                    matrix_rag[3][1] += 1
                elif result_isUtility == 3:
                    y_pred_rag.append(2)
                    y_pred.append(2)
                    matrix_rag[3][2] += 1
                elif result_isUtility == 4:
                    y_pred_rag.append(3)
                    y_pred.append(3)
                    matrix_rag[3][3] += 1
                elif result_isUtility == 5:
                    y_pred_rag.append(4)
                    y_pred.append(4)
                    matrix_rag[3][4] += 1
                else:
                    y_pred_rag.append(5)
                    y_pred.append(5)
                    matrix_rag[3][5] += 1

            elif isUtility == '[Utility:5]':
                y_true_rag.append(4)
                y_true.append(4)
                if result_isUtility == 1:
                    y_pred_rag.append(0)
                    y_pred.append(0)
                    matrix_rag[4][0] += 1
                elif result_isUtility == 2:
                    y_pred_rag.append(1)
                    y_pred.append(1)
                    matrix_rag[4][1] += 1
                elif result_isUtility == 3:
                    y_pred_rag.append(2)
                    y_pred.append(2)
                    matrix_rag[4][2] += 1
                elif result_isUtility == 4:
                    y_pred_rag.append(3)
                    y_pred.append(3)
                    matrix_rag[4][3] += 1
                elif result_isUtility == 5:
                    y_pred_rag.append(4)
                    y_pred.append(4)
                    matrix_rag[4][4] += 1
                else:
                    y_pred_rag.append(5)
                    y_pred.append(5)
                    matrix_rag[4][5] += 1
        else: # 不执行检索，所以直接使用生成数据

            output = data['SA_RAG_data_no_ret'][0]
            isUtility = data['isUtility']
            result_isUtility = count_isUtility(output)

            if isUtility == '[Utility:1]':
                y_true_no_rag.append(0)
                y_true.append(0)
                if result_isUtility == 1:
                    y_pred_no_rag.append(0)
                    y_pred.append(0)
                    matrix_no_rag[0][0] += 1
                elif result_isUtility == 2:
                    y_pred_no_rag.append(1)
                    y_pred.append(1)
                    matrix_no_rag[0][1] += 1
                elif result_isUtility == 3:
                    y_pred_no_rag.append(2)
                    y_pred.append(2)
                    matrix_no_rag[0][2] += 1
                elif result_isUtility == 4:
                    y_pred_no_rag.append(3)
                    y_pred.append(3)
                    matrix_no_rag[0][3] += 1
                elif result_isUtility == 5:
                    y_pred_no_rag.append(4)
                    y_pred.append(4)
                    matrix_no_rag[0][4] += 1
                else:
                    y_pred_no_rag.append(5)
                    y_pred.append(5)
                    matrix_no_rag[0][5] += 1

            elif isUtility == '[Utility:2]':
                y_true_no_rag.append(1)
                y_true.append(1)
                if result_isUtility == 1:
                    y_pred_no_rag.append(0)
                    y_pred.append(0)
                    matrix_no_rag[1][0] += 1
                elif result_isUtility == 2:
                    y_pred_no_rag.append(1)
                    y_pred.append(1)
                    matrix_no_rag[1][1] += 1
                elif result_isUtility == 3:
                    y_pred_no_rag.append(2)
                    y_pred.append(2)
                    matrix_no_rag[1][2] += 1
                elif result_isUtility == 4:
                    y_pred_no_rag.append(3)
                    y_pred.append(3)
                    matrix_no_rag[1][3] += 1
                elif result_isUtility == 5:
                    y_pred_no_rag.append(4)
                    y_pred.append(4)
                    matrix_no_rag[1][4] += 1
                else:
                    y_pred_no_rag.append(5)
                    y_pred.append(5)
                    matrix_no_rag[1][5] += 1

            elif isUtility == '[Utility:3]':
                y_true_no_rag.append(2)
                y_true.append(2)
                if result_isUtility == 1:
                    y_pred_no_rag.append(0)
                    y_pred.append(0)
                    matrix_no_rag[2][0] += 1
                elif result_isUtility == 2:
                    y_pred_no_rag.append(1)
                    y_pred.append(1)
                    matrix_no_rag[2][1] += 1
                elif result_isUtility == 3:
                    y_pred_no_rag.append(2)
                    y_pred.append(2)
                    matrix_no_rag[2][2] += 1
                elif result_isUtility == 4:
                    y_pred_no_rag.append(3)
                    y_pred.append(3)
                    matrix_no_rag[2][3] += 1
                elif result_isUtility == 5:
                    y_pred_no_rag.append(4)
                    y_pred.append(4)
                    matrix_no_rag[2][4] += 1
                else:
                    y_pred_no_rag.append(5)
                    y_pred.append(5)
                    matrix_no_rag[2][5] += 1

            elif isUtility == '[Utility:4]':
                y_true_no_rag.append(3)
                y_true.append(3)
                if result_isUtility == 1:
                    y_pred_no_rag.append(0)
                    y_pred.append(0)
                    matrix_no_rag[3][0] += 1
                elif result_isUtility == 2:
                    y_pred_no_rag.append(1)
                    y_pred.append(1)
                    matrix_no_rag[3][1] += 1
                elif result_isUtility == 3:
                    y_pred_no_rag.append(2)
                    y_pred.append(2)
                    matrix_no_rag[3][2] += 1
                elif result_isUtility == 4:
                    y_pred_no_rag.append(3)
                    y_pred.append(3)
                    matrix_no_rag[3][3] += 1
                elif result_isUtility == 5:
                    y_pred_no_rag.append(4)
                    y_pred.append(4)
                    matrix_no_rag[3][4] += 1
                else:
                    y_pred_no_rag.append(5)
                    y_pred.append(5)
                    matrix_no_rag[3][5] += 1

            elif isUtility == '[Utility:5]':
                y_true_no_rag.append(4)
                y_true.append(4)
                if result_isUtility == 1:
                    y_pred_no_rag.append(0)
                    y_pred.append(0)
                    matrix_no_rag[4][0] += 1
                elif result_isUtility == 2:
                    y_pred_no_rag.append(1)
                    y_pred.append(1)
                    matrix_no_rag[4][1] += 1
                elif result_isUtility == 3:
                    y_pred_no_rag.append(2)
                    y_pred.append(2)
                    matrix_no_rag[4][2] += 1
                elif result_isUtility == 4:
                    y_pred_no_rag.append(3)
                    y_pred.append(3)
                    matrix_no_rag[4][3] += 1
                elif result_isUtility == 5:
                    y_pred_no_rag.append(4)
                    y_pred.append(4)
                    matrix_no_rag[4][4] += 1
                else:
                    y_pred_no_rag.append(5)
                    y_pred.append(5)
                    matrix_no_rag[4][5] += 1

    print()
    print('执行检索的程序，加入检索信息之后生成的数据')
    print('意义说明： 第一行为真实的数据，分别是：[Utility:1]、[Utility:2]、[Utility:3]、[Utility:4]、[Utility:5]、Error')
    matrix_rag = pd.DataFrame(matrix_rag)
    print(matrix_rag)
    print()
    print(classification_report(y_true_rag, y_pred_rag, target_names=['Utility:1', 'Utility:4', 'Utility:5', 'Error']))
    print()
    print('不执行检索，所以直接使用生成数据')
    print('意义说明： 第一行为真实的数据，分别是：[Utility:1]、[Utility:2]、[Utility:3]、[Utility:4]、[Utility:5]、Error')
    matrix_no_rag = pd.DataFrame(matrix_no_rag)
    print(matrix_no_rag)
    print()
    print(classification_report(y_true_no_rag, y_pred_no_rag, target_names=['Utility:4', 'Utility:5', 'Error']))
    print()
    print('-------------------------------------')
    print(classification_report(y_true, y_pred, target_names=['Utility:1', 'Utility:4', 'Utility:5', 'Error']))





if __name__ == "__main__":
    print("\nstart:\n\n")
    main()
    print("\n\nend!!!\n\n")





