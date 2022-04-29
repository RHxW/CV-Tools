import cv2
import os
import tqdm
import numpy as np


def stat_calc_single_dir(dir_path):
    # calculate the statistic values(mean, standard variance) of RGB images in one dir
    if not os.path.exists(dir_path):
        return None
    if dir_path[-1] != '/':
        dir_path += '/'

    file_names = os.listdir(dir_path)
    rgb_mean = np.array([0, 0, 0], dtype=np.float32)
    rgb_std = np.array([0, 0, 0], dtype=np.float32)
    n = 0
    for name in tqdm.tqdm(file_names):
        if name.split('.')[-1] not in ['jpeg', 'jpg', 'png']:
            continue
        img_path = dir_path + name
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.array(img, dtype=np.float32) / 255
        rgb_mean += np.array([np.mean(img[:, :, 0]), np.mean(img[:, :, 1]), np.mean(img[:, :, 2])])
        rgb_std += np.array([np.std(img[:, :, 0]), np.std(img[:, :, 1]), np.std(img[:, :, 2])])
        n += 1

    rgb_mean /= n
    rgb_std /= n

    return rgb_mean, rgb_std
