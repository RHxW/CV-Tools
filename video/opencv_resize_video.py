import cv2
import os

# video = cv2.VideoWriter('ss.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (width,height)) #创建视频流对象-格式二

"""
参数1 即将保存的文件路径
参数2 VideoWriter_fourcc为视频编解码器
    fourcc意为四字符代码（Four-Character Codes），顾名思义，该编码由四个字符组成,下面是VideoWriter_fourcc对象一些常用的参数,注意：字符顺序不能弄混
    cv2.VideoWriter_fourcc('I', '4', '2', '0'),该参数是YUV编码类型，文件名后缀为.avi 
    cv2.VideoWriter_fourcc('P', 'I', 'M', 'I'),该参数是MPEG-1编码类型，文件名后缀为.avi 
    cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'),该参数是MPEG-4编码类型，文件名后缀为.avi 
    cv2.VideoWriter_fourcc('T', 'H', 'E', 'O'),该参数是Ogg Vorbis,文件名后缀为.ogv 
    cv2.VideoWriter_fourcc('F', 'L', 'V', '1'),该参数是Flash视频，文件名后缀为.flv
    cv2.VideoWriter_fourcc('m', 'p', '4', 'v')    文件名后缀为.mp4
参数3 为帧播放速率
参数4 (width,height)为视频帧大小
"""


def video_resize(video_path, save_path, save_size):
    """
    因为opencv读视频可能会将视频旋转90度，所以先padding 再resize 最后手动旋转
    :param video_path:
    :param save_path:
    :param save_size: H,W
    :return:
    """
    assert os.path.exists(video_path)
    assert type(save_size) in [tuple, list]
    assert len(save_size) == 2

    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(5))  # 获取帧率
    H = int(cap.get(4))
    W = int(cap.get(3))

    videowriter = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, save_size)

    # success, _ = cap.read()
    if H > W:
        top = 0
        bottom = 0
        left = (H - W) // 2
        right = H - W - left
    else:
        top = (W - H) // 2
        bottom = W - H - top
        left = 0
        right = 0

    success = True
    while success:
        success, img1 = cap.read()
        try:
            imgp = cv2.copyMakeBorder(img1, top, bottom, left, right, cv2.BORDER_CONSTANT, value=0)  # padding
            img = cv2.resize(imgp, save_size, interpolation=cv2.INTER_LINEAR)  # 按比例缩放

            videowriter.write(img)
        except:
            break


if __name__ == "__main__":
    video_path = "C:/Users/Admin/Downloads/lixiang2.mp4"
    save_path = "C:/Users/Admin/Downloads/256.mp4"
    save_size = (256, 256)
    video_resize(video_path, save_path, save_size)
