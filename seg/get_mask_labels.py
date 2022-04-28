import numpy as np


def get_mask_labels(label_img, cls_num):
    h, w, c = label_img.shape
    label_img = label_img[:, :, 0]  # (h, w)
    label_gt = np.zeros([cls_num, h, w], dtype=np.uint8)

    for i in range(cls_num):
        mask_cur = np.where(label_img == i)
        label_gt[i, :, :][mask_cur] = 1

    return label_gt
