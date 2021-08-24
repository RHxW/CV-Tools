import cv2
import copy

def face_anno_vis(img, faces, box_color=(0, 255, 255), lmk_color=(0, 255, 0)):
    """

    :param img: cv2/numpy object
    :param faces: [[face1box, face1landmarks], [face2box, face2landmarks], ...]
    :return:
    """
    if not img:
        return
    if not isinstance(faces, list):
        raise RuntimeError("faces type error!")
    if not faces:
        return img

    anno_img = copy.deepcopy(img)
    for i, face_anno in enumerate(faces):
        if len(face_anno) != 2:
            print(" length of face_anno in faces != 2")
            return anno_img
        _box, _lmks = face_anno
        x1, y1, x2, y2 = _box
        cv2.rectangle(anno_img, (x1, y1), (x2, y2), box_color, 1)
        for p1, p2 in _lmks:
            cv2.circle(anno_img, (int(p1), int(p2)), 1, lmk_color, thickness=2)

    return anno_img