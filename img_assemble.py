import cv2
import os
import numpy as np

from resize import ImageResizePad


def img_assemble(img_dirs_root, save_dir, img_size=(-1, -1), N=-1):
    """
    图像拼接，按文件夹（有序）整理
    :param img_dirs_root: 文件夹图片按顺序组成一行
    :param save_dir: 图片保存文件夹
    :param img_size: 图片缩放尺寸(H, W)，如果全部是-1则按第一个文件夹中第一张图片尺寸缩放，如果只有一个-1则用另一个尺寸代替((100,-1)--->(100,100))
    :param N: N行生成一张组合后的图片，如果是-1则全部拼接成一张
    :return:
    """
    if not os.path.exists(img_dirs_root):
        raise RuntimeError("img_dirs_root not exists!")
    if img_dirs_root[-1] != "/":
        img_dirs_root += "/"

    img_paths = []
    img_counts = []
    for img_dir in os.listdir(img_dirs_root):
        sub_paths = []
        dir_path = img_dirs_root + img_dir + "/"
        for name in os.listdir(dir_path):
            sub_paths.append(dir_path + name)
        img_paths.append(sub_paths)
        img_counts.append(len(sub_paths))

    if len(set(img_counts)) != 1:
        print("dir image number: ", img_counts)
        raise RuntimeError("image number error!")

    if N > img_counts[0] or N <= 0:  # 每张大图一共有多少行
        N = img_counts[0]

    M = len(img_paths)  # 一共有多少个文件夹，即列的数量
    if type(img_size) not in [list, tuple] or len(img_size) != 2:
        raise RuntimeError("img_size error")
    img_size = list(img_size)
    if img_size[0] <= 0 and img_size[1] <= 0:
        img_size[0], img_size[1], _ = cv2.imread(img_paths[0][0]).shape
    elif img_size[0] <= 0:
        img_size[0] = img_size[1]
    elif img_size[1] <= 0:
        img_size[1] = img_size[0]

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    if save_dir[-1] != "/":
        save_dir += "/"

    count = 1
    while img_paths[0]:
        tmp_img_paths = []
        for i in range(M):
            tmp_img_paths.append(img_paths[i][:N])
            img_paths[i] = img_paths[i][N:]

        # 计算每张大图的尺寸
        H = len(tmp_img_paths[0]) * img_size[0]
        W = M * img_size[1]

        # 生成空白大图
        final_matrix = np.zeros((H, W, 3), np.uint8)

        for i in range(len(tmp_img_paths[0])):
            for j in range(M):
                # 第i行第j列
                _path = tmp_img_paths[j][i]
                _img = cv2.imread(_path)
                _img, padding_shape = ImageResizePad(_img, img_size, 0)
                final_matrix[i * img_size[0]:(i + 1) * img_size[0], j * img_size[1]:(j + 1) * img_size[1], :] = _img

        cv2.imwrite(save_dir + "%d.png" % count, final_matrix)
        count += 1


if __name__ == "__main__":
    img_dirs_root = "F:/3DMMProjects/Rotate-and-Render-master/results/rs_model/example/as/"
    save_dir = "F:/3DMMProjects/Rotate-and-Render-master/results/rs_model/example/"
    img_assemble(img_dirs_root, save_dir, img_size=(224, -1), N=4)
