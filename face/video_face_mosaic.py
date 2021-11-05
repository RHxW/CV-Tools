import cv2


def face_msk(video_path, save_path):
    cap = cv2.VideoCapture(video_path)  # 打开摄像头（0/1/2代表摄像头编号0.1.2）
    fps = int(cap.get(5))  # 获取帧率
    H = int(cap.get(4))
    W = int(cap.get(3))
    save_size = (H, W)
    videowriter = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, save_size)

    xml_path = 'D:/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(xml_path)  # 创建一个级联分类器对象(包含大数据训练的人脸特征)
    success = True
    while (success):
        try:
            success, frame = cap.read()  # 读一帧
            # frame = cv2.flip(frame, 1)  # 镜头翻转（1水平，0垂直，-1水平垂直）
            # cv2.imshow('a',frame)
            # cv2.waitKey()
            # cv2.destroyAllWindows()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 人脸识别必须转化为灰阶图像
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.07,
                                                  minNeighbors=5)  # (图，每次图像缩小比例（根据人脸大小），每个目标检测次数阈值 )
            for x, y, w, h, in faces:
                # print("x = %d,y = %d,w = %d,h = %d"%(x,y,w,h))
                for m in range(y, y + h):  # y
                    for n in range(x, x + w):  # x
                        if m % 10 == 0 and n % 10 == 0:  # 将10 * 10的方格内的像素颜色，设置与[m,n]点颜色相同
                            for i in range(10):
                                for j in range(10):
                                    (b, g, r) = frame[m, n]
                                    frame[i + m, j + n] = (b, g, r)
            cv2.imshow("1", frame)
            cv2.waitKey()
            cv2.destroyAllWindows()
                # if c == 27:  # ESC按键
                #     cv2.destroyAllWindows()
                #     break
            videowriter.write(frame)
        except:
            break

if __name__ == "__main__":
    video_path = 'C:/Users/Admin/Documents/WeChat Files/a40981790/FileStorage/Video/2021-10/1.mp4'
    save_path = 'C:/Users/Admin/Documents/WeChat Files/a40981790/FileStorage/Video/2021-10/2.mp4'
    face_msk(video_path, save_path)