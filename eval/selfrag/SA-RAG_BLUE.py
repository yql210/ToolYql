import json
import jsonlines
import re
import spacy
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu
from nltk.translate.bleu_score import SmoothingFunction
import platform
import os


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


def clear_all_tokens(model_answer):

    # [# 正则表达式 - 语法](https://www.runoob.com/regexp/regexp-syntax.html)
    # [正则表达式-在线测试工具](https://www.jyshare.com/front-end/854/)
    model_answer = re.sub(r'\[.*?]', '', model_answer)
    model_answer = re.sub(r'\<.*?>', '', model_answer)

    return model_answer


def play_sound():
    system = platform.system()
    if system == "Windows":
        import winsound
        winsound.Beep(500, 5000)
    elif system == "Linux" or system == "Darwin":
        os.system("play -nq -t alsa synth {} sine {}".format(1, 1000))


def split_sentences(paragraph):
    doc = nlp(paragraph)
    # sentences = []
    # for sent in doc.sents:
    #     sentences.append(sent.text)
    sentences1 = []
    for sent in doc:
        sentences1.append(sent.text)

    return sentences1


nlp = spacy.load("zh_core_web_sm")


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

    # 开始测试数据集对其影响
    # file_path = './sa-self-gen-data-after-retrieval/0410_sa_rag_1.3b_epcoh_3_data_0_2_after_retrieval.jsonl'
    # file_path = './sa-self-gen-data-after-retrieval/0410_sa_rag_1.3b_epcoh_3_data_0_4_after_retrieval.jsonl'
    # file_path = './sa-self-gen-data-after-retrieval/0410_sa_rag_1.3b_epcoh_3_data_0_6_after_retrieval.jsonl'
    # file_path = './sa-self-gen-data-after-retrieval/0410_sa_rag_1.3b_epcoh_3_data_0_8_after_retrieval.jsonl'
    # file_path = './sa-self-gen-data-after-retrieval/0410_sa_rag_1.3b_epcoh_3_data_alone_spcql_after_retrieval.jsonl'

    # 开始测试
    file_path = './sa-self-gen-data/chinese-llama-2-1.3b.jsonl'
    file_path_train = './sa-self-gen-data/chatglm3-6b.jsonl'

    file_path = './sa-self-gen-data-after-retrieval/chinese-llama-2-1.3b.jsonl'

    # file_path = './sa-self-gen-data/chinese-llama-2-7b.jsonl'
    # file_path = './sa-self-gen-data/chinese-llama-2-13b.jsonl'

    # file_path = './sa-self-gen-data-after-retrieval/chinese-llama-2-7b.jsonl'
    file_path = './sa-self-gen-data-after-retrieval/chinese-llama-2-13b.jsonl'

    file_path = './sa-self-gen-data-after-retrieval/0506_sa_rag_1.3b_epcoh_3_only_output_after_retrieval.jsonl'

    file_path = './sa-self-gen-data-after-retrieval/0530_sa_rag_1.3b_epcoh_3_no_retrieval_after_retrieval.jsonl'
    file_path = './sa-self-gen-data-after-retrieval/0530_sa_rag_1.3b_epcoh_3_no_label_after_retrieval.jsonl'
    file_path = './sa-self-gen-data-after-retrieval/0530_0405_sa_rag_1.3b_epcoh_3_no_retrieval_after_retrieval.jsonl'
    file_path = './sa-self-gen-data-after-retrieval/0530_0530_sa_rag_1.3b_epcoh_3_no_label_no_retrieval_after_retrieval.jsonl'
    file_path = './sa-self-gen-data-after-retrieval/0530_0530_sa_rag_1.3b_epcoh_3_no_label_no_retrieval_after_retrieval_1.jsonl'
    file_path = './sa-self-gen-data-after-retrieval/0530_0530_sa_rag_1.3b_epcoh_3_no_label_all_retrieval_after_retrieval_2.jsonl'


    input_datas = load_file(file_path)
    input_datas_train = load_file(file_path_train)

    reference = []  # 给定标准译文
    candidate = []  # 神经网络生成的句子

    smooth = SmoothingFunction()  # 定义平滑函数对象

    BLUE_1 = 0
    BLUE_2 = 0
    BLUE_3 = 0
    BLUE_4 = 0
    BLUE_Num = 0

    Ret_BLUE_1 = 0
    Ret_BLUE_2 = 0
    Ret_BLUE_3 = 0
    Ret_BLUE_4 = 0
    Ret_BLUE_Num = 0

    No_Ret_BLUE_1 = 0
    No_Ret_BLUE_2 = 0
    No_Ret_BLUE_3 = 0
    No_Ret_BLUE_4 = 0
    No_Ret_BLUE_Num = 0

    # for data, data_train in zip(input_datas, input_datas_train):
    #     print(data)
    #
    #     if data['Retrieval'] == "[Retrieval]":
    #         Ret_BLUE_Num += 1
    #         BLUE_Num += 1
    #         str_ref = data['answer']
    #         str_gen = data_train['Output']
    #         # str_gen = data['SA_RAG_data'][0]
    #         str_gen_clear = clear_all_tokens(str_gen)
    #         print(str_ref)
    #         print(str_gen)
    #         print(str_gen_clear)
    #
    #         str_ref_split = split_sentences(str_ref)
    #         str_gen_clear_split = split_sentences(str_gen_clear)
    #         print(str_ref_split)
    #         print(str_gen_clear_split)
    #
    #         reference.append(str_ref_split)
    #         candidate = str_gen_clear_split
    #         # candidate.append(str_gen_clear_split)
    #         Ret_BLUE_1 += sentence_bleu(reference, candidate, weights=(1, 0, 0, 0), smoothing_function=smooth.method1)
    #         Ret_BLUE_2 += sentence_bleu(reference, candidate, weights=(0, 1, 0, 0), smoothing_function=smooth.method1)
    #         Ret_BLUE_3 += sentence_bleu(reference, candidate, weights=(0, 0, 1, 0), smoothing_function=smooth.method1)
    #         Ret_BLUE_4 += sentence_bleu(reference, candidate, weights=(0, 0, 0, 1), smoothing_function=smooth.method1)
    #
    #         BLUE_1 += sentence_bleu(reference, candidate, weights=(1, 0, 0, 0), smoothing_function=smooth.method1)
    #         BLUE_2 += sentence_bleu(reference, candidate, weights=(0, 1, 0, 0), smoothing_function=smooth.method1)
    #         BLUE_3 += sentence_bleu(reference, candidate, weights=(0, 0, 1, 0), smoothing_function=smooth.method1)
    #         BLUE_4 += sentence_bleu(reference, candidate, weights=(0, 0, 0, 1), smoothing_function=smooth.method1)
    #
    #         reference.clear()
    #         # print('Cumulate 1-gram :%f' \
    #         #       % Ret_BLUE_1)
    #         # print('Cumulate 2-gram :%f' \
    #         #       % Ret_BLUE_2)
    #         # print('Cumulate 3-gram :%f' \
    #         #       % Ret_BLUE_3)
    #         # print('Cumulate 4-gram :%f' \
    #         #       % Ret_BLUE_4)
    #
    #
    #     else:
    #         No_Ret_BLUE_Num += 1
    #         BLUE_Num += 1
    #         str_ref = data['answer']
    #         str_gen = data_train['Output']
    #         str_gen_clear = clear_all_tokens(str_gen)
    #         print(str_ref)
    #         print(str_gen)
    #         print(str_gen_clear)
    #
    #         str_ref_split = split_sentences(str_ref)
    #         str_gen_clear_split = split_sentences(str_gen_clear)
    #         print(str_ref_split)
    #         print(str_gen_clear_split)
    #
    #         reference.append(str_ref_split)
    #         candidate = str_gen_clear_split
    #         # candidate.append(str_gen_clear_split)
    #         No_Ret_BLUE_1 += sentence_bleu(reference, candidate, weights=(1, 0, 0, 0), smoothing_function=smooth.method1)
    #         No_Ret_BLUE_2 += sentence_bleu(reference, candidate, weights=(0, 1, 0, 0), smoothing_function=smooth.method1)
    #         No_Ret_BLUE_3 += sentence_bleu(reference, candidate, weights=(0, 0, 1, 0), smoothing_function=smooth.method1)
    #         No_Ret_BLUE_4 += sentence_bleu(reference, candidate, weights=(0, 0, 0, 1), smoothing_function=smooth.method1)
    #
    #         BLUE_1 += sentence_bleu(reference, candidate, weights=(1, 0, 0, 0), smoothing_function=smooth.method1)
    #         BLUE_2 += sentence_bleu(reference, candidate, weights=(0, 1, 0, 0), smoothing_function=smooth.method1)
    #         BLUE_3 += sentence_bleu(reference, candidate, weights=(0, 0, 1, 0), smoothing_function=smooth.method1)
    #         BLUE_4 += sentence_bleu(reference, candidate, weights=(0, 0, 0, 1), smoothing_function=smooth.method1)
    #
    #         reference.clear()
    #         # print('Cumulate 1-gram :%f' \
    #         #       % No_Ret_BLUE_1)
    #         # print('Cumulate 2-gram :%f' \
    #         #       % No_Ret_BLUE_2)
    #         # print('Cumulate 3-gram :%f' \
    #         #       % No_Ret_BLUE_3)
    #         # print('Cumulate 4-gram :%f' \
    #         #       % No_Ret_BLUE_4)
    #
    #     print('end')


    for data in input_datas:
        print(data)

        if data['Retrieval'] == "[Retrieval]":
            Ret_BLUE_Num += 1
            BLUE_Num += 1
            str_ref = data['answer']
            # str_gen = data['SA_RAG_data_no_ret'][0]
            str_gen = data['SA_RAG_data'][0]
            str_gen_clear = clear_all_tokens(str_gen)
            print(str_ref)
            print(str_gen)
            print(str_gen_clear)

            str_ref_split = split_sentences(str_ref)
            str_gen_clear_split = split_sentences(str_gen_clear)
            print(str_ref_split)
            print(str_gen_clear_split)

            reference.append(str_ref_split)
            candidate = str_gen_clear_split
            # candidate.append(str_gen_clear_split)
            Ret_BLUE_1 += sentence_bleu(reference, candidate, weights=(1, 0, 0, 0), smoothing_function=smooth.method1)
            Ret_BLUE_2 += sentence_bleu(reference, candidate, weights=(0, 1, 0, 0), smoothing_function=smooth.method1)
            Ret_BLUE_3 += sentence_bleu(reference, candidate, weights=(0, 0, 1, 0), smoothing_function=smooth.method1)
            Ret_BLUE_4 += sentence_bleu(reference, candidate, weights=(0, 0, 0, 1), smoothing_function=smooth.method1)

            BLUE_1 += sentence_bleu(reference, candidate, weights=(1, 0, 0, 0), smoothing_function=smooth.method1)
            BLUE_2 += sentence_bleu(reference, candidate, weights=(0, 1, 0, 0), smoothing_function=smooth.method1)
            BLUE_3 += sentence_bleu(reference, candidate, weights=(0, 0, 1, 0), smoothing_function=smooth.method1)
            BLUE_4 += sentence_bleu(reference, candidate, weights=(0, 0, 0, 1), smoothing_function=smooth.method1)

            reference.clear()
            # print('Cumulate 1-gram :%f' \
            #       % Ret_BLUE_1)
            # print('Cumulate 2-gram :%f' \
            #       % Ret_BLUE_2)
            # print('Cumulate 3-gram :%f' \
            #       % Ret_BLUE_3)
            # print('Cumulate 4-gram :%f' \
            #       % Ret_BLUE_4)


        else:
            No_Ret_BLUE_Num += 1
            BLUE_Num += 1
            str_ref = data['answer']
            # str_gen = data['SA_RAG_data_no_ret'][0]
            str_gen = data['SA_RAG_data'][0]
            str_gen_clear = clear_all_tokens(str_gen)
            print(str_ref)
            print(str_gen)
            print(str_gen_clear)

            str_ref_split = split_sentences(str_ref)
            str_gen_clear_split = split_sentences(str_gen_clear)
            print(str_ref_split)
            print(str_gen_clear_split)

            reference.append(str_ref_split)
            candidate = str_gen_clear_split
            # candidate.append(str_gen_clear_split)
            No_Ret_BLUE_1 += sentence_bleu(reference, candidate, weights=(1, 0, 0, 0), smoothing_function=smooth.method1)
            No_Ret_BLUE_2 += sentence_bleu(reference, candidate, weights=(0, 1, 0, 0), smoothing_function=smooth.method1)
            No_Ret_BLUE_3 += sentence_bleu(reference, candidate, weights=(0, 0, 1, 0), smoothing_function=smooth.method1)
            No_Ret_BLUE_4 += sentence_bleu(reference, candidate, weights=(0, 0, 0, 1), smoothing_function=smooth.method1)

            BLUE_1 += sentence_bleu(reference, candidate, weights=(1, 0, 0, 0), smoothing_function=smooth.method1)
            BLUE_2 += sentence_bleu(reference, candidate, weights=(0, 1, 0, 0), smoothing_function=smooth.method1)
            BLUE_3 += sentence_bleu(reference, candidate, weights=(0, 0, 1, 0), smoothing_function=smooth.method1)
            BLUE_4 += sentence_bleu(reference, candidate, weights=(0, 0, 0, 1), smoothing_function=smooth.method1)

            reference.clear()
            # print('Cumulate 1-gram :%f' \
            #       % No_Ret_BLUE_1)
            # print('Cumulate 2-gram :%f' \
            #       % No_Ret_BLUE_2)
            # print('Cumulate 3-gram :%f' \
            #       % No_Ret_BLUE_3)
            # print('Cumulate 4-gram :%f' \
            #       % No_Ret_BLUE_4)

        print('end')

    print("所有数据数据，以下是相关的BLUE数据：")
    print('Cumulate 1-gram :%f' \
          % (BLUE_1 / BLUE_Num))
    print('Cumulate 2-gram :%f' \
          % (BLUE_2 / BLUE_Num))
    print('Cumulate 3-gram :%f' \
          % (BLUE_3 / BLUE_Num))
    print('Cumulate 4-gram :%f' \
          % (BLUE_4 / BLUE_Num))
    print(BLUE_Num)

    print("执行检索生成的数据，以下是相关的BLUE数据：")
    print('Cumulate 1-gram :%f' \
          % (Ret_BLUE_1 / Ret_BLUE_Num))
    print('Cumulate 2-gram :%f' \
          % (Ret_BLUE_2 / Ret_BLUE_Num))
    print('Cumulate 3-gram :%f' \
          % (Ret_BLUE_3 / Ret_BLUE_Num))
    print('Cumulate 4-gram :%f' \
          % (Ret_BLUE_4 / Ret_BLUE_Num))
    print(Ret_BLUE_Num)

    print("不需要检索生成的数据，以下是相关的BLUE数据：")
    print('Cumulate 1-gram :%f' \
          % (No_Ret_BLUE_1 / No_Ret_BLUE_Num))
    print('Cumulate 2-gram :%f' \
          % (No_Ret_BLUE_2 / No_Ret_BLUE_Num))
    print('Cumulate 3-gram :%f' \
          % (No_Ret_BLUE_3 / No_Ret_BLUE_Num))
    print('Cumulate 4-gram :%f' \
          % (No_Ret_BLUE_4 / No_Ret_BLUE_Num))
    print(No_Ret_BLUE_Num)


if __name__ == "__main__":
    print("\nstart:\n\n")
    main()
    print("\n\nend!!!\n\n")
    play_sound()





