import os
import cv2
import shutil


def size_filter(img_root, min_h, min_w=0, max_h=float("inf"), max_w=float("inf"), mode="h", is_delete=True,
                is_copy=False, copy_dir="") -> list or None:
    if img_root[-1] != "/":
        img_root += "/"
    if not os.path.exists(img_root):
        return
    imgs = os.listdir(img_root)
    N = len(imgs)
    if mode not in ["h", "w", "both"]:
        raise RuntimeError("invalid mode")
    if mode in ["h", "both"]:
        min_h = max(min_h, 0)
        if min_h >= max_h or max_h <= 0:
            raise RuntimeError("invalid Height range")

    if mode in ["w", "both"]:
        min_w = max(min_w, 0)
        if min_w >= max_w or max_w <= 0:
            raise RuntimeError("invalid Width range")

    if not is_delete ^ is_copy:
        raise RuntimeError("Delete <OR> Copy! OR!!! At least ONE!!!")
    if is_copy and not copy_dir:
        raise RuntimeError("invalid copy_dir")

    img_retain = []  # image retained
    for i in range(N):
        _img_name = imgs[i]
        _img = cv2.imread(img_root + _img_name)
        H, W, C = _img.shape
        flg = False  # True: remove, False: retain
        if mode in ["h", "both"]:
            if not min_h <= H <= max_h:
                flg = True
        if mode in ["w", "both"]:
            if not min_w <= W <= max_w:
                flg = True
        if flg:
            continue
        else:
            img_retain.append(_img_name)

    if is_delete:
        for _ in list(set(imgs) - set(img_retain)):
            os.remove(img_root + _)
    elif is_copy:
        if copy_dir[-1] != "/":
            copy_dir += "/"
        if not os.path.exists(copy_dir):
            os.mkdir(copy_dir)
        for _ in img_retain:
            shutil.copy(img_root + _, copy_dir + _)

    return img_retain
