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


def dataset_partition(ratios: list, dataset_origin: list, inplace: bool = False):
    """
    数据集按任意比例划分
    :param ratios:
    :param dataset_origin:
    :param inplace:
    :return:
    """
    total_ratio = sum(ratios)
    if total_ratio < 1:
        ratios.append((1 - total_ratio))
    elif total_ratio > 1:
        raise RuntimeError('total ratio greater than 1 !!!')

    assert isinstance(dataset_origin, list)

    n = len(dataset_origin)
    counts = []
    for r in ratios[:-1]:
        counts.append(int(n * r))
    counts.append(n - sum(counts))

    if inplace:
        dataset = dataset_origin
    else:
        dataset = copy.deepcopy(dataset_origin)
    random.shuffle(dataset)

    partitions = []

    start_idx = 0
    for c in counts[:-1]:
        partitions.append(dataset[start_idx:start_idx + c])
        start_idx += c

    partitions.append(dataset[start_idx:])

    return partitions