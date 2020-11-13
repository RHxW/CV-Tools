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

