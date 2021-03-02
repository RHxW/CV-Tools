import cv2
import numpy as np


class Flip(object):
    # 在图像的水平和垂直轴上随机执行翻转
    def __call__(self, X):
        for axis in [0, 1]:
            if np.random.rand(1) < 0.5:
                X = np.flip(X, axis)
        return X


class Crop(object):
    # 在随机区域上裁剪了一部分随机大小的图像
    def __init__(self, min_size_ratio, max_size_ratio=(1, 1)):
        self.min_size_ratio = np.array(list(min_size_ratio))
        self.max_size_ratio = np.array(list(max_size_ratio))

    def __call__(self, X):
        size = np.array(X.shape[:2])
        mini = self.min_size_ratio * size
        maxi = self.max_size_ratio * size
        # random size
        h = np.random.randint(mini[0], maxi[0])
        w = np.random.randint(mini[1], maxi[1])
        # random place
        shift_h = np.random.randint(0, size[0] - h)
        shift_w = np.random.randint(0, size[1] - w)
        X = X[shift_h:shift_h + h, shift_w:shift_w + w]

        return X


class Sharpen(object):
    # 锐化
    def __init__(self, max_center=4):
        self.identity = np.array([[0, 0, 0],
                                  [0, 1, 0],
                                  [0, 0, 0]])
        self.sharpen = np.array([[0, -1, 0],
                                 [-1, 4, -1],
                                 [0, -1, 0]]) / 4
        self.max_center = max_center

    def __call__(self, X):
        sharp = self.sharpen * np.random.random() * self.max_center
        kernel = self.identity + sharp

        X = cv2.filter2D(X, -1, kernel)
        return X


class AverageBlur(object):
    # 平均模糊
    def __init__(self, max_kernel=(7, 7)):
        self.max_kernel = ((np.array(max_kernel) + 1) // 2)

    def __call__(self, X):
        kernel_size = (
            np.random.randint(1, self.max_kernel[0]) * 2 + 1,
            np.random.randint(1, self.max_kernel[1]) * 2 + 1,
        )
        X = cv2.GaussianBlur(X, kernel_size, 0)
        return X


class GaussianBlur(object):
    # 高斯模糊
    def __init__(self, max_kernel=(7, 7)):
        self.max_kernel = max_kernel

    def __call__(self, X):
        kernel_size = [
            np.random.randint(1, self.max_kernel[0] + 1),
            np.random.randint(1, self.max_kernel[1] + 1),
        ]
        if kernel_size[0] % 2 == 0:
            kernel_size[0] += 1
        if kernel_size[1] % 2 == 0:
            kernel_size[1] += 1
        X = cv2.GaussianBlur(X, tuple(kernel_size), 0)
        return X


class Perspective(object):
    # 透视变换(旋转，平移，剪切和缩放)
    def __init__(self,
                 max_ratio_translation=(0.2, 0.2, 0),
                 max_rotation=(10, 10, 360),
                 max_scale=(0.1, 0.1, 0.2),
                 max_shearing=(15, 15, 5)):
        self.max_ratio_translation = np.array(max_ratio_translation)
        self.max_rotation = np.array(max_rotation)
        self.max_scale = np.array(max_scale)
        self.max_shearing = np.array(max_shearing)

    def __call__(self, X):
        # get the height and the width of the image
        h, w = X.shape[:2]
        max_translation = self.max_ratio_translation * np.array([w, h, 1])
        # get the values on each axis
        t_x, t_y, t_z = np.random.uniform(-1, 1, 3) * max_translation
        r_x, r_y, r_z = np.random.uniform(-1, 1, 3) * self.max_rotation
        sc_x, sc_y, sc_z = np.random.uniform(-1, 1, 3) * self.max_scale + 1
        sh_x, sh_y, sh_z = np.random.uniform(-1, 1, 3) * self.max_shearing

        # convert degree angles to rad
        theta_rx = np.deg2rad(r_x)
        theta_ry = np.deg2rad(r_y)
        theta_rz = np.deg2rad(r_z)
        theta_shx = np.deg2rad(sh_x)
        theta_shy = np.deg2rad(sh_y)
        theta_shz = np.deg2rad(sh_z)

        # compute its diagonal
        diag = (h ** 2 + w ** 2) ** 0.5
        # compute the focal length
        f = diag
        if np.sin(theta_rz) != 0:
            f /= 2 * np.sin(theta_rz)

        # set the image from cartesian to projective dimension
        H_M = np.array([[1, 0, -w / 2],
                        [0, 1, -h / 2],
                        [0, 0, 1],
                        [0, 0, 1]])
        # set the image projective to cartesian dimension
        Hp_M = np.array([[f, 0, w / 2, 0],
                         [0, f, h / 2, 0],
                         [0, 0, 1, 0]])

        # adjust the translation on z
        t_z = (f - t_z) / sc_z ** 2
        # translation matrix to translate the image
        T_M = np.array([[1, 0, 0, t_x],
                        [0, 1, 0, t_y],
                        [0, 0, 1, t_z],
                        [0, 0, 0, 1]])

        # calculate cos and sin of angles
        sin_rx, cos_rx = np.sin(theta_rx), np.cos(theta_rx)
        sin_ry, cos_ry = np.sin(theta_ry), np.cos(theta_ry)
        sin_rz, cos_rz = np.sin(theta_rz), np.cos(theta_rz)
        # get the rotation matrix on x axis
        R_Mx = np.array([[1, 0, 0, 0],
                         [0, cos_rx, -sin_rx, 0],
                         [0, sin_rx, cos_rx, 0],
                         [0, 0, 0, 1]])
        # get the rotation matrix on y axis
        R_My = np.array([[cos_ry, 0, -sin_ry, 0],
                         [0, 1, 0, 0],
                         [sin_ry, 0, cos_ry, 0],
                         [0, 0, 0, 1]])
        # get the rotation matrix on z axis
        R_Mz = np.array([[cos_rz, -sin_rz, 0, 0],
                         [sin_rz, cos_rz, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])
        # compute the full rotation matrix
        R_M = np.dot(np.dot(R_Mx, R_My), R_Mz)

        # get the scaling matrix
        Sc_M = np.array([[sc_x, 0, 0, 0],
                         [0, sc_y, 0, 0],
                         [0, 0, sc_z, 0],
                         [0, 0, 0, 1]])

        # get the tan of angles
        tan_shx = np.tan(theta_shx)
        tan_shy = np.tan(theta_shy)
        tan_shz = np.tan(theta_shz)
        # get the shearing matrix on x axis
        Sh_Mx = np.array([[1, 0, 0, 0],
                          [tan_shy, 1, 0, 0],
                          [tan_shz, 0, 1, 0],
                          [0, 0, 0, 1]])
        # get the shearing matrix on y axis
        Sh_My = np.array([[1, tan_shx, 0, 0],
                          [0, 1, 0, 0],
                          [0, tan_shz, 1, 0],
                          [0, 0, 0, 1]])
        # get the shearing matrix on z axis
        Sh_Mz = np.array([[1, 0, tan_shx, 0],
                          [0, 1, tan_shy, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])
        # compute the full shearing matrix
        Sh_M = np.dot(np.dot(Sh_Mx, Sh_My), Sh_Mz)

        Identity = np.array([[1, 0, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 1, 0],
                             [0, 0, 0, 1]])

        # compute the full transform matrix
        M = Identity
        M = np.dot(Sh_M, M)
        M = np.dot(R_M, M)
        M = np.dot(Sc_M, M)
        M = np.dot(T_M, M)
        M = np.dot(Hp_M, np.dot(M, H_M))
        # apply the transformation
        X = cv2.warpPerspective(X, M, (w, h))
        return X


class Cutout(object):
    def __init__(self,
                 min_size_ratio,
                 max_size_ratio,
                 channel_wise=False,
                 max_crop=10,
                 replacement=0):
        self.min_size_ratio = np.array(list(min_size_ratio))
        self.max_size_ratio = np.array(list(max_size_ratio))
        self.channel_wise = channel_wise
        self.max_crop = max_crop
        self.replacement = replacement

    def __call__(self, X):
        size = np.array(X.shape[:2])
        mini = self.min_size_ratio * size
        maxi = self.max_size_ratio * size
        for _ in range(self.max_crop):
            # random size
            h = np.random.randint(mini[0], maxi[0])
            w = np.random.randint(mini[1], maxi[1])
            # random place
            shift_h = np.random.randint(0, size[0] - h)
            shift_w = np.random.randint(0, size[1] - w)
            if self.channel_wise:
                c = np.random.randint(0, X.shape[-1])
                X[shift_h:shift_h + h, shift_w:shift_w + w, c] = self.replacement
            else:
                X[shift_h:shift_h + h, shift_w:shift_w + w] = self.replacement
        return X


class Brightness(object):
    # 亮度
    def __init__(self, range_brightness=(-50, 50)):
        self.range_brightness = range_brightness

    def __call__(self, X):
        brightness = np.random.randint(*self.range_brightness)
        X = X + brightness
        return X


class Contrast(object):
    # 对比度
    def __init__(self, range_contrast=(-50, 50)):
        self.range_contrast = range_contrast

    def __call__(self, X):
        contrast = np.random.randint(*self.range_contrast)
        X = X * (contrast / 127 + 1) - contrast
        return X


class UniformNoise(object):
    def __init__(self, low=-50, high=50):
        self.low = low
        self.high = high

    def __call__(self, X):
        noise = np.random.uniform(self.low, self.high, X.shape)
        X = X + noise
        return X


class GaussianNoise(object):
    def __init__(self, center=0, std=50):
        self.center = center
        self.std = std

    def __call__(self, X):
        noise = np.random.normal(self.center, self.std, X.shape)
        X = X + noise
        return X


class Vignetting(object):
    # 渐晕效果
    def __init__(self,
                 ratio_min_dist=0.2,
                 range_vignette=(0.2, 0.8),
                 random_sign=False):
        self.ratio_min_dist = ratio_min_dist
        self.range_vignette = np.array(range_vignette)
        self.random_sign = random_sign

    def __call__(self, X):
        h, w = X.shape[:2]
        min_dist = np.array([h, w]) / 2 * np.random.random() * self.ratio_min_dist

        # create matrix of distance from the center on the two axis
        x, y = np.meshgrid(np.linspace(-w / 2, w / 2, w), np.linspace(-h / 2, h / 2, h))
        x, y = np.abs(x), np.abs(y)

        # create the vignette mask on the two axis
        x = (x - min_dist[0]) / (np.max(x) - min_dist[0])
        x = np.clip(x, 0, 1)
        y = (y - min_dist[1]) / (np.max(y) - min_dist[1])
        y = np.clip(y, 0, 1)

        # then get a random intensity of the vignette
        vignette = (x + y) / 2 * np.random.uniform(*self.range_vignette)
        vignette = np.tile(vignette[..., None], [1, 1, 3])

        sign = 2 * (np.random.random() < 0.5) * (self.random_sign) - 1
        X = X * (1 + sign * vignette)

        return X


class LensDistortion(object):
    # 镜头变形
    # 径向系数k1，k2，k3和切向系数p1，p2
    # 系数的顺序如下：k1，k2，p1，p2，k3
    def __init__(self, d_coef=(0.15, 0.15, 0.1, 0.1, 0.05)):
        self.d_coef = np.array(d_coef)

    def __call__(self, X):
        # get the height and the width of the image
        h, w = X.shape[:2]

        # compute its diagonal
        f = (h ** 2 + w ** 2) ** 0.5

        # set the image projective to carrtesian dimension
        K = np.array([[f, 0, w / 2],
                      [0, f, h / 2],
                      [0, 0, 1]])

        d_coef = self.d_coef * np.random.random(5)  # value
        d_coef = d_coef * (2 * (np.random.random(5) < 0.5) - 1)  # sign
        # Generate new camera matrix from parameters
        M, _ = cv2.getOptimalNewCameraMatrix(K, d_coef, (w, h), 0)

        # Generate look-up tables for remapping the camera image
        remap = cv2.initUndistortRectifyMap(K, d_coef, None, M, (w, h), 5)

        # Remap the original image to a new image
        X = cv2.remap(X, *remap, cv2.INTER_LINEAR)
        return X
