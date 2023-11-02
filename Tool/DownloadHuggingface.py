
from datasets import load_dataset

data_files = {
    'finetune': 'finetune\\test_en_1.json'}

dataset = load_dataset("shibing624/medical", revision="main", data_dir="finetune", data_files=data_files)


# dataset = load_dataset('medical', 'pretrain')
dataset.save_to_disk('./dataset/shibing624/medical')

#
#
# # #加载数据集.
# # import datasets
# # dataset = datasets.load_from_disk("dataset/neulab/conala")




# from datasets import load_dataset
#
# raw_datasets = load_dataset("allocine")
# raw_datasets.cache_files


