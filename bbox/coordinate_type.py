import numpy as np
import torch


class CoordinateConvertor:
    def __init__(self):
        self.types = ['CHW', 'XY_LT', 'XY_LB']
        # 'CHW': [center_x, center_y, w, h]
        # 'XY_LT': [x_min, y_max, x_max, y_min]  left top & right bottom
        # 'XY_LB': [x_min, y_min, x_max, y_max]  left bottom & right top

        self.chw2xylt = CWH2XYLT
        self.chw2xylb = CWH2XYLB
        self.xylt2chw = XYLT2CWH
        self.xylb2chw = XYLB2CWH

    def convert(self, boxes, origin_type, dest_type):
        assert origin_type in self.types and dest_type in self.types
        assert len(boxes.shape) == 2
        if origin_type == dest_type:
            print('Types does not change.')
            return boxes
        if origin_type == 'CHW':
            if dest_type == 'XY_LT':
                return self.chw2xylt(boxes)
            elif dest_type == 'XY_LB':
                return self.chw2xylb(boxes)
        else:
            if origin_type == 'XY_LT':
                return self.xylt2chw(boxes)
            elif origin_type == 'XY_LB':
                return self.xylb2chw(boxes)

        return None

def CWH2XYLT(boxes):
    """
    (cx, cy, w, h) -> [x_min, y_max, x_max, y_min]  left top & right bottom
    :param boxes: [box_num, 4]
    :return:
    """
    assert boxes.shape[-1] == 4
    cx = boxes[:, 0]
    cy = boxes[:, 1]
    w = boxes[:, 2]
    h = boxes[:, 3]

    half_w = torch.div(w, 2, rounding_mode='floor')
    half_h = torch.div(h, 2, rounding_mode='floor')

    x_min = cx - half_w
    y_min = cy - half_h
    x_max = cx + half_w
    y_max = cy + half_h

    return torch.clamp(torch.stack([x_min, y_max, x_max, y_min]).t(), min=0)


def CWH2XYLB(boxes):
    """
    (cx, cy, w, h) -> [x_min, y_min, x_max, y_max]  left bottom & right top
    :param boxes: [box_num, 4]
    :return:
    """
    assert boxes.shape[-1] == 4
    cx = boxes[:, 0]
    cy = boxes[:, 1]
    w = boxes[:, 2]
    h = boxes[:, 3]

    half_w = torch.div(w, 2, rounding_mode='floor')
    half_h = torch.div(h, 2, rounding_mode='floor')

    x_min = cx - half_w
    y_min = cy - half_h
    x_max = cx + half_w
    y_max = cy + half_h

    return torch.clamp(torch.stack([x_min, y_min, x_max, y_max]).t(), min=0)


def XYLT2CWH(boxes):
    """
    [x_min, y_max, x_max, y_min] -> (cx, cy, w, h)  left top 2 center
    :param boxes: [box_num, 4]
    :return:
    """
    assert boxes.shape[-1] == 4
    x_min = boxes[:, 0]
    y_max = boxes[:, 1]
    x_max = boxes[:, 2]
    y_min = boxes[:, 3]

    w = x_max - x_min
    h = y_max - y_min

    cx = torch.div((x_min + x_max), 2, rounding_mode='floor')
    cy = torch.div((y_min + y_max), 2, rounding_mode='floor')

    return torch.stack([cx, cy, w, h]).t()


def XYLB2CWH(boxes):
    """
    [x_min, y_min, x_max, y_max] -> (cx, cy, w, h)  left bottom 2 center
    :param boxes: [box_num, 4]
    :return:
    """
    assert boxes.shape[-1] == 4
    x_min = boxes[:, 0]
    y_min = boxes[:, 1]
    x_max = boxes[:, 2]
    y_max = boxes[:, 3]

    w = x_max - x_min
    h = y_max - y_min

    cx = torch.div((x_min + x_max), 2, rounding_mode='floor')
    cy = torch.div((y_min + y_max), 2, rounding_mode='floor')

    return torch.stack([cx, cy, w, h]).t()
