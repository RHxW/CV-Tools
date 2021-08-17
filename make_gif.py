import os
from PIL import Image
import imageio

def save_gif_PIL(img_dir, save_name):
    if not os.path.exists(img_dir):
        return
    if img_dir[-1] != "/":
        img_dir += "/"
    images = []
    for name in os.listdir(img_dir):
        images.append(Image.open(img_dir+name))

    im = images[0]
    images = images[1:]
    if len(save_name) <= 4 or save_name[:-4] != ".gif":
        save_name += ".gif"
    im.save(save_name, save_all=True, append_images=images, loop=0, duration=1, comment=b"aaabb")


def save_gif_imageio(img_dir, save_name):
    if not os.path.exists(img_dir):
        return
    if img_dir[-1] != "/":
        img_dir += "/"
    images = []
    for name in os.listdir(img_dir):
        images.append(imageio.imread(img_dir+name))
    if len(save_name) <= 4 or save_name[:-4] != ".gif":
        save_name += ".gif"
    imageio.mimsave(save_name, images, duration=1)  # imageio.help('GIF')