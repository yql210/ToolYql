
def count_true(gold_answer, model_answer):
    count_gold_num = 0
    count_model_num = 0
    count_model_num_true = 0
    count_model_num_false = 0

    length_gold = len(gold_answer)
    length_model = len(model_answer)

    # 创建一个空集合用于存储唯一的value键
    gold_value_set = set()

    for dict_gold_answer in gold_answer:
        # 假设每个字典只有一个键值对
        for key, value in dict_gold_answer.items():
            # 将value值添加到集合中
            gold_value_set.add(value)
            count_gold_num += 1

    for dict_model_answer in model_answer:
        for key, value in dict_model_answer.items():
            count_model_num += 1
            if value in gold_value_set:
                count_model_num_true += 1
                gold_value_set.remove(value)
            else:
                count_model_num_false += 1

    if count_gold_num != length_gold:
        print("原始数据集中，length_gold与count_gold_num个数不同。分别是： ", count_gold_num, " --", length_gold)

    if count_model_num != length_model:
        print("在生成的数据集中，length_model与count_model_num个数不同。分别是： ", count_model_num, " --", length_model)

    result = {}
    result['count_gold_num'] = count_gold_num
    result['count_model_num'] = count_model_num
    result['count_model_num_true'] = count_model_num_true
    result['count_model_num_false'] = count_model_num_false
    result['length_gold'] = length_gold
    result['length_model'] = length_model
    result['set_isEmpty'] = len(gold_value_set) == 0

    return result


# gold_answer = [{'p.name': '记者'}, {'p.name': '模特儿'}, {'p.name': '军官'}]
# model_answer = [{'m.name': '记者', 'p.name': '记者1'}, {'m.name': '模特儿'}, {'m.name': '军官'}]

gold_answer = [{'m.name': '千明勋', 'n.name': '韩国首尔'}, {'m.name': '千明勋', 'n.name': '韩国首尔'}, {'m.name': '金烔完', 'n.name': '韩国'}, {'m.name': '金烔完', 'n.name': '韩国'}, {'m.name': '李秉宪', 'n.name': '汉城（今首尔）'}]
model_answer = [{'m.name': '千明勋', 'n.name': '韩国首尔'}, {'m.name': '千明勋', 'n.name': '韩国首尔'}, {'m.name': '金烔完', 'n.name': '韩国'}, {'m.name': '金烔完', 'n.name': '韩国'}, {'m.name': '李秉宪', 'n.name': '汉城（今首尔）'}]

res = count_true(gold_answer, model_answer)
print(res)
