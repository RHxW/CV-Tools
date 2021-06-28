import cv2
import numpy as np

def jpg_compress(img_path, ratio, is_save=True, save_root=""):
    img = cv2.imread(img_path)
    # 取值范围：0~100，数值越小，压缩比越高，图片质量损失越严重
    params = [cv2.IMWRITE_JPEG_QUALITY, ratio]  # ratio:0~100
    msg = cv2.imencode(".jpg", img, params)[1]
    msg = (np.array(msg)).tobytes()
    print("msg:", len(msg))

    if is_save:
        new_name = img_path.split("/")[-1].split(".")[0] + "_%d" % ratio + ".jpg"
        if not save_root:
            save_root = "./"
        if save_root[-1] != "/":
            save_root += "/"
        new_path = save_root + new_name
        cv2.imwrite(new_path, img, params)


def png_compress(img_path, ratio, is_save=True, save_root=""):
    img = cv2.imread(img_path)
    # 取值范围：0~9，数值越小，压缩比越低，图片质量越高
    params = [cv2.IMWRITE_PNG_COMPRESSION, ratio]  # ratio: 0~9
    msg = cv2.imencode(".png", img, params)[1]
    msg = (np.array(msg)).tobytes()
    print("msg:", len(msg))

    if is_save:
        new_name = img_path.split("/")[-1].split(".")[0] + "_%d" % ratio + ".png"
        if not save_root:
            save_root = "./"
        if save_root[-1] != "/":
            save_root += "/"
        new_path = save_root + new_name
        cv2.imwrite(new_path, img, params)