#! -*- coding: utf-8 -*-
import numpy as np
import cv2
import copy
import struct

FLT_EPSILON=1e-5

def saveNumpy(fname, data):
    sdata = copy.deepcopy(data)
    sdata = sdata.flatten()
    num_len = sdata.shape[0]
    with open(fname, 'wb') as nStream:
        bytei = struct.pack('i', num_len)
        nStream.write(bytei)
        for i in range(num_len):
            bytef = struct.pack('f', sdata[i])
            nStream.write(bytef)
        nStream.flush()
    return


def getTransMatrix(fpoints, std_points):
    trans = np.zeros((2, 3))
    points_num = 5.
    sum_x, sum_y = np.sum(std_points, axis=0)
    sum_u, sum_v = np.sum(fpoints, axis=0)
    sum_xx_yy = np.sum(std_points**2)
    sum_ux_vy = np.sum(std_points*fpoints)
    vx_uy = fpoints[:, ::-1]*std_points
    sum_vx__uy = np.sum(vx_uy[:, 0] - vx_uy[:, 1])
    # print("sum_x: ", sum_x)
    # print("sum_y: ", sum_y)
    # print("sum_u: ", sum_u)
    # print("sum_v: ", sum_v)
    # print("sum_xx_yy: ", sum_xx_yy)
    # print("sum_ux_vy: ", sum_ux_vy)
    # print("sum_vx__uy: ", sum_vx__uy)

    if sum_xx_yy <= FLT_EPSILON:
        return None

    q = sum_u - sum_x * sum_ux_vy / sum_xx_yy + sum_y * sum_vx__uy / sum_xx_yy
    p = sum_v - sum_y * sum_ux_vy / sum_xx_yy - sum_x * sum_vx__uy / sum_xx_yy
    r = points_num - (sum_x * sum_x + sum_y * sum_y) / sum_xx_yy
    if not (r > FLT_EPSILON or r < -FLT_EPSILON):
        return None
    a = (sum_ux_vy - sum_x * q / r - sum_y * p / r) / sum_xx_yy
    b = (sum_vx__uy + sum_y * q / r - sum_x * p / r) / sum_xx_yy
    c = q / r
    d = p / r

    trans[0, 0] = trans[1, 1] = a
    trans[0, 1] = -b
    trans[1, 0] = b
    trans[0, 2] = c
    trans[1, 2] = d
    # trans = trans[::-1,:]

    return trans


def alignFace(fimage, fmarks, scale=1.0):
    assert fimage.ndim >= 2
    assert fmarks.shape[0] == 5 and fmarks.shape[1] == 2
    h, w = fimage.shape[:2]
    scale_x = float(w)/float(96)
    scale_y = float(h)/float(112)
    std_marks = np.array([

    30.2946, 51.6963,
    65.5318, 51.5014,
    48.0252, 71.7366,
    33.5493, 92.3655,
    62.7299, 92.2041

    ], dtype=np.float).reshape(5, 2)
    # print(std_marks)

    std_marks *= [scale_x, scale_y]
    tranMatrix = getTransMatrix(std_marks, fmarks)
    tranMatrix = tranMatrix.astype(np.float)

    if tranMatrix is not None:
        if scale == 1.0:
            res_image = cv2.warpAffine(fimage, tranMatrix, dsize=(w, h))
        else:
            nw, nh = int(scale*float(w)), int(scale*float(h))
            mw, mh = int((scale-1.)*float(w/2.)), int((scale-1.)*float(h/(2.)))
            tranMatrix[0, 2] += mw  # move to right
            tranMatrix[1, 2] += mh
            res_image = cv2.warpAffine(fimage, tranMatrix, dsize=(nw, nh))
    else:
        return None, None

    return res_image, tranMatrix
