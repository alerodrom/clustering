from os import path, listdir

from cv2 import imread, calcHist
from matplotlib import pyplot as plt


# EJEMPLO MODIFICADO
def recorre_imagenes(self):
    input_path = 'input'
    list_frames = {}
    i = 0
    for image in listdir(input_path):
        img_path = path.join(input_path, image)
        img = imread(img_path)
        # imshow('image', img)
        # print(img_path)
        color = ('b', 'g', 'r')
        for col in enumerate(color):
            hist_b = calcHist([img], [0], None, [256], [0, 256])
            hist_g = calcHist([img], [1], None, [256], [0, 256])
            hist_r = calcHist([img], [2], None, [256], [0, 256])
            # print('Color ' + str(col) + str(hist_b))
            # plt.plot(hist_b, color=col)
            # plt.plot(hist_g, color=col)
            # plt.plot(hist_r, color=col)
            hist_values = [hist_b, hist_g, hist_r]
            plt.xlim([0, 256])
        list_frames.update({image: hist_values})
        i += 1
        if i == 3:
            # print(list_frames)
            break
