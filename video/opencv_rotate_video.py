import cv2
import os


def video_rotate(video_path, save_path, rotate_direction, rotate_angle):
    """

    :param video_path:
    :param save_path:
    :param rotate_direction: clockwise(1) or anticlockwise(2)
    :param rotate_angle: 90(1), 180(2) or 270(3)
    :return:
    """
    assert os.path.exists(video_path)
    assert rotate_direction in [1, 2]
    assert rotate_angle in [1, 2, 3]

    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(5))  # 获取帧率
    H = int(cap.get(4))
    W = int(cap.get(3))
    videowriter = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (H, W))

    center = (W // 2, H // 2)
    angle = rotate_angle * 90
    if rotate_direction == 2:
        angle = 0 - angle
    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    success = True
    while success:
        success, img1 = cap.read()
        try:
            rotated = cv2.warpAffine(img1, M, (W, H))
            videowriter.write(rotated)
        except:
            break

if __name__ == "__main__":
    video_path = "C:/Users/Admin/Downloads/lixiang2.mp4"
    save_path = "C:/Users/Admin/Downloads/lixiang2R.mp4"
    rotate_direction = 1
    rotate_angle = 1
    video_rotate(video_path, save_path, rotate_direction, rotate_angle)