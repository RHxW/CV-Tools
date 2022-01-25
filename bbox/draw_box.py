import cv2
import copy


def draw_box(img, boxes, box_color=(0, 255, 255)):
    """
    在图片上画box
    :param img:
    :param boxes: [[x1, y1, x2, y2]...]  左上和右下点的坐标
    :param color:
    :return:
    """
    anno_img = copy.deepcopy(img)
    for box in boxes:
        x1, y1, x2, y2 = box
        cv2.rectangle(anno_img, (x1, y1), (x2, y2), box_color, 1)

    return anno_img
