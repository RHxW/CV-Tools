import torch


def get_intersection(A_boxes, B_boxes):
    """
    Calculating the intersection part of two input boxes(A & B)
    :param A_boxes: [A, 4] [x_min, y_min, x_max, y_max]  这里是左下点和右上点的坐标
    :param B_boxes: [B, 4] [x_min, y_min, x_max, y_max]  这里是左下点和右上点的坐标
    :return: [A, B] value of intersections
    """
    A = A_boxes.shape[0]
    B = B_boxes.shape[0]

    max_xy = torch.min(A_boxes[:, 2:].unsqueeze(1).expand(A, B, 2),
                       B_boxes[:, 2:].unsqueeze(0).expand(A, B, 2))  # right top
    min_xy = torch.max(A_boxes[:, :2].unsqueeze(1).expand(A, B, 2),
                       B_boxes[:, :2].unsqueeze(0).expand(A, B, 2))  # left bottom

    inter = torch.clamp((max_xy - min_xy), min=0)
    return inter[:, :, 0] * inter[:, :, 1]  # width * height


def get_area(boxes):
    """
    Calculating the area of boxes
    :param boxes: [box_num, 4] [x_min, y_min, x_max, y_max]  这里是左下点和右上点的坐标
    :return: [box_num, 1] value of area
    """
    w = boxes[:, 2] - boxes[:, 0]
    h = boxes[:, 3] - boxes[:, 1]
    return (w * h).unsqueeze(-1)


def jaccard(A_boxes, B_boxes):
    """
    Compute the jaccard/IOU value of two sets of boxes(cross).
    :param A_boxes: [A, 4] [x_min, y_min, x_max, y_max]  左下点和右上点的坐标
    :param B_boxes: [B, 4] [x_min, y_min, x_max, y_max]  左下点和右上点的坐标
    :return: [A, B]
    """
    inter = get_intersection(A_boxes, B_boxes)
    area_A = get_area(A_boxes)
    area_B = get_area(B_boxes)
    union = area_A + area_B - inter
    return inter / union # [A, B]
