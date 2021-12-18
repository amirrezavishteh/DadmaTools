import json
import os
from base import DatasetInfo, BaseDataset
from dataset_utils import is_exist_dataset, unzip_dataset, download_dataset, DEFAULT_CACHE_DIR

URL = 'https://raw.githubusercontent.com/HaniehP/PersianNER/master/ArmanPersoNERCorpus.zip'
DATASET_NAME = "ARMAN"


def ARMAN(dest_dir=DEFAULT_CACHE_DIR):
    base_addr = os.path.dirname(__file__)
    info_addr = os.path.join(base_addr, 'info.json')
    DATASET_INFO = json.load(open(info_addr))
    dest_dir = os.path.join(dest_dir, DATASET_NAME)

    def get_arman_item(dir_addr, split):
        f_addr = os.path.join(dir_addr, split)
        f = open(f_addr)
        sentence = []
        for line in f:
            if len(line) == 0 or line.startswith('-DOCSTART') or line[0] == "\n":
                if len(sentence) > 0:
                    yield sentence
                    sentence = []
                continue
            splits = line.split(' ')
            sentence.append([splits[0], splits[-1].rstrip("\n")])

        if len(sentence) > 0:
            yield sentence
            sentence = []

    if not is_exist_dataset(DATASET_INFO, dest_dir):
        downloaded_file = download_dataset(URL, dest_dir)
        dest_dir = unzip_dataset(downloaded_file, dest_dir)

    train_iterator = get_arman_item(dest_dir, 'train_fold1.txt')
    test_dataset = get_arman_item(dest_dir, 'test_fold1.txt')
    # dev_iterator = get_arman_item(dir_addr, 'dev')
    # train = BaseDataset(train_iterator)
    # test = BaseDataset(test_iterator)

    info = DatasetInfo(info_addr=info_addr)
    train_dataset = BaseDataset(train_iterator,info)
    test_dataset = BaseDataset(test_dataset,info)
    return {'train': train_dataset, 'test': test_dataset}
