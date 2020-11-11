import cv2
from copy import deepcopy


def ImageResizeScale(
        image,
        scale_x: float or int,
        scale_y: float or int,
        in_place: bool = False
):
    """
    resize image at given scales
    :param image:
    :param scale_x:
    :param scale_y:
    :param in_place:
    :return:
    """
    if not image:
        return None
    if in_place:
        img = image
    else:
        img = deepcopy(image)

    for _s in (scale_x, scale_y):
        if type(_s) not in [float, int]:
            raise RuntimeError("scale type should be float or int")
        if _s < 0:
            raise RuntimeError("scale can't be negative")

    img = cv2.resize(img, None, None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_LINEAR)

    return img


def ImageResizePad(
        image,
        dst_size: int or tuple or list,
        padding_val: int or tuple or list,
        keep_aspect_ratio: bool = True,
        in_place: bool = False
):
    if not image:
        return None
    # check dst_size type and values
    if type(dst_size) in [int, tuple, list]:
        if type(dst_size) is int:
            dst_size = (dst_size, dst_size)
        else:
            dst_size = tuple(dst_size)
        if len(dst_size) != 2:
            raise RuntimeError("length of dst_size should be 2, in HW order")
        for _ds in dst_size:
            if type(_ds) is not int:
                raise RuntimeError("H and W of dst_size should be int")
            if _ds < 0:
                raise RuntimeError("dst_size can't be negative")
    else:
        raise RuntimeError("dst_size should be int or tuple or list type")

    # check padding_val type and values
    if type(padding_val) in [int, tuple, list]:
        if type(padding_val) is int:
            padding_val = (padding_val, padding_val, padding_val)
        else:
            if len(padding_val) != 3:
                raise RuntimeError("length of padding_val should be 3, in BGR order")
            padding_val = tuple(padding_val)
        for _pv in padding_val:
            if _pv < 0 or _pv > 255:
                raise RuntimeError("invalid padding_val: " + str(padding_val))
    else:
        raise RuntimeError("padding_val should be int or tuple or list type")

    H, W, C = image.shape()
    if in_place:
        img = image
    else:
        img = deepcopy(image)

    pt, pb, pl, pr = 0, 0, 0, 0  # top, bottom, left, right
    if keep_aspect_ratio:
        pass  # TODO
    else:
        img = cv2.resize(img, dst_size[0], dst_size[1], interpolation=cv2.INTER_LINEAR)  # TODO dst_size order???xy or yx
        padding = (pt, pb, pl, pr)

    return img, padding
