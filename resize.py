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
    if image is None:
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
        padding: bool = True,
        in_place: bool = False
):
    if image is None:
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
    if padding:
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

    H, W, C = image.shape
    if in_place:
        img = image
    else:
        img = deepcopy(image)

    # resize and padding
    pt, pb, pl, pr = 0, 0, 0, 0  # padding_shape: top, bottom, left, right
    if keep_aspect_ratio:
        # if dst_size[0] != dst_size[1]:
        #     print("if keep aspect ratio, dst size should be same with H and W.")

        # resize 按最长边
        # if H > W:
        #     long_side = H
        #     img_size = dst_size[0]
        # else:
        #     long_side = W
        #     img_size = dst_size[1]

        h_ratio = dst_size[0] / H
        w_ratio = dst_size[1] / W
        resize_scale = min(h_ratio, w_ratio)
        # long_side = max(H, W)
        # img_size = dst_size[0]
        # resize = long_side / img_size
        # if h_ratio < w_ratio:  # based on resized H, padding W
        #     pl = (img_size - image.shape[1]) // 2
        #     pr = img_size - image.shape[1] - pl
        # else:
        #     pt = (img_size - image.shape[0]) // 2
        #     pb = img_size - image.shape[0] - pt
        if resize_scale != 1:
            # interp_methods = [cv2.INTER_LINEAR, cv2.INTER_CUBIC, cv2.INTER_AREA, cv2.INTER_NEAREST, cv2.INTER_LANCZOS4]
            # interp_method = interp_methods[random.randrange(5)]
            img = cv2.resize(img, None, None, fx=resize_scale, fy=resize_scale, interpolation=cv2.INTER_LINEAR)
        if h_ratio > w_ratio:  # padding W
            pl = (dst_size[1] - img.shape[1]) // 2
            pr = dst_size[1] - img.shape[1] - pl
        else:
            pt = (dst_size[0] - img.shape[0]) // 2
            pb = dst_size[0] - img.shape[0] - pt

        # padding constant
        if padding:
            img = cv2.copyMakeBorder(img, pt, pb, pl, pr, cv2.BORDER_CONSTANT, value=padding_val)
    else:
        img = cv2.resize(img, dst_size[0], dst_size[1],
                         interpolation=cv2.INTER_LINEAR)  # TODO dst_size order???xy or yx
    padding_shape = (pt, pb, pl, pr)

    return img, padding_shape
