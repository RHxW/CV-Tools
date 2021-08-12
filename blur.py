import cv2
import numpy as np
import random
import copy
import os


def gaussianNoise(image, ksize=13, degree=None):
    row, col, ch = image.shape
    mean = 0
    if not degree:
        var = np.random.uniform(0.004, 0.01)
    else:
        var = degree
    sigma = var  # ** 0.5
    noisy = cv2.GaussianBlur(image, (ksize, ksize), sigmaX=sigma, sigmaY=sigma)
    return noisy


def defocus(img, degree=13):
    # degree = np.random.randint(3, 10)
    # if degree %2 ==0:
    #    degree +=1
    defocus_image = cv2.GaussianBlur(img, ksize=(degree, degree), sigmaX=0, sigmaY=0)
    return defocus_image


def motionBlur(image, degree=10):
    """
    degree : 1 ~ 9
    """
    angle = random.randint(1, 360)
    # image = np.array(image)
    # 这里生成任意角度的运动模糊kernel的矩阵,  degree越大，模糊程度越高
    M = cv2.getRotationMatrix2D((degree / 2, degree / 2), angle, 1)
    motion_blur_kernel = np.diag(np.ones(degree))
    motion_blur_kernel = cv2.warpAffine(motion_blur_kernel, M, (degree, degree))

    motion_blur_kernel = motion_blur_kernel / degree
    blurred = cv2.filter2D(image, -1, motion_blur_kernel)
    # convert to uint8
    cv2.normalize(blurred, blurred, 0, 255, cv2.NORM_MINMAX)
    blurred = np.array(blurred, dtype=np.uint8)
    return blurred


def lowLevelsize(img, level=None):
    """
    level : 0 ~ 6
    """
    h, w = img.shape[:2]
    if level is not None:
        scale_factor = level
    else:
        scale_factor = np.random.randint(0, 6)
    ssize = max(w - 8 * scale_factor, 12)
    dsized = cv2.resize(img, (ssize, ssize))
    fsized = cv2.resize(dsized, (w, h))
    return fsized

##马赛克
def do_mosaic(frame, x, y, w, h, neighbor=9):
    """
    马赛克的实现原理是把图像上某个像素点一定范围邻域内的所有点用邻域内左上像素点的颜色代替，这样可以模糊细节，但是可以保留大体的轮廓。
    :param frame: opencv frame
    :param int x :  马赛克左顶点
    :param int y:  马赛克右顶点
    :param int w:  马赛克宽
    :param int h:  马赛克高
    :param int neighbor:  马赛克每一块的宽
    """
    fh, fw = frame.shape[0], frame.shape[1]
    if (y + h > fh) or (x + w > fw):
        return
    for i in range(0, h - neighbor, neighbor):  # 关键点0 减去neighbour 防止溢出
        for j in range(0, w - neighbor, neighbor):
            rect = [j + x, i + y, neighbor, neighbor]
            color = frame[i + y][j + x].tolist()  # 关键点1 tolist
            left_up = (rect[0], rect[1])
            right_down = (rect[0] + neighbor - 1, rect[1] + neighbor - 1)  # 关键点2 减去一个像素
            cv2.rectangle(frame, left_up, right_down, color, -1)
    return frame

def mosaic_full(img, neighbor):
    x, y = 0, 0
    h, w, c = img.shape
    return do_mosaic(img, x, y, w, h, neighbor)