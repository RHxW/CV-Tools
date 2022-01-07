import random
import copy


def train_test_dataset_partition(trainset_ratio: float, dataset_all: list, remain_origin: bool = True):
    """
    训练集和测试级按比例划分
    :param trainset_ratio:
    :param dataset_all:
    :param remain_origin:
    :return:
    """
    assert isinstance(trainset_ratio, float) and 0 < trainset_ratio < 1
    assert isinstance(dataset_all, list)

    n = len(dataset_all)
    train_n = int(n * trainset_ratio)

    if remain_origin:
        dataset = copy.deepcopy(dataset_all)
    else:
        dataset = dataset_all

    random.shuffle(dataset)
    train_set = dataset[:train_n]
    test_set = dataset[train_n:]
    return train_set, test_set