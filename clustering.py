from os import path, listdir

import numpy as np
from cv2 import imread, calcHist, VideoCapture, CAP_PROP_FPS, imwrite, VideoWriter, destroyAllWindows, \
    VideoWriter_fourcc
from matplotlib import pyplot as plt


def get_frames_from_video(video):
    vidcap = VideoCapture(video)
    success, image = vidcap.read()
    fps = int(vidcap.get(CAP_PROP_FPS))
    count = 0
    success = True
    cont_aux = 0
    while success:
        success, image = vidcap.read()
        if count % fps == 0:
            cont_aux += 1
            imwrite('input/frame%03d.jpg' % cont_aux, image)
        count += 1


def get_video_from_frames():
    img = []
    input_path = 'output'
    for image in sorted(listdir(input_path)):
        img_path = path.join(input_path, image)
        img.append(imread(img_path))
    height, width, layers = img[1].shape
    mp4 = VideoWriter_fourcc(*'XVID')
    video = VideoWriter('resume.avi', mp4, 1, (width, height))
    for i in img:
        video.write(i)


# EJEMPLO MODIFICADO
def recorre_imagenes():
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


def get_key_frames(input_path, t, k, h):
    list_frames = {}
    n = len(listdir(input_path))
    f = 1
    for image in listdir(input_path):
        if f == 1 or f <= n:
            img_path = path.join(input_path, image)
            img = imread(img_path)
            hist_b = calcHist([img.ravel()], [0], None, [256], h)
            # hist_g = calcHist([img], [1], None, [256], h)
            # hist_r = calcHist([img], [2], None, [256], h)
            # list_hist = [hist_b, hist_g, hist_r]
            f += t
        list_frames.update({image: hist_b})
        # print(list_frames)
        # APLICA K-MEDIAS
        list_frames_classified = aplica_kmedias(list_frames, k)
        # list_key_frames = calcula_centroides_clases(list_frames_classified, k)
        # print(list(list_frames.keys())[0])
        # print(list(list_frames.values())[0])
        # return [list_frames_classified, list_key_frames]


def aplica_kmedias(list_frames, k):
    list_frames_classified = {}
    for k, v in list_frames.items():
        print(k)
        for frame in v.tolist():
            print(frame)
            break
            key = min([(i[0], np.linalg.norm(float(frame) - k[i[0]])) for i in enumerate(k)], key=lambda t: t[1])[0]
            # try:
            #     list_frames_classified[key].append(frame)
            # except KeyError:
            #     list_frames_classified[key] = [frame]
    return list_frames_classified


def calcula_centroides_clases(list_frames_classified, k):
    return True


# get_key_frames('input', 1, 0, [0, 256])
get_frames_from_video('video.mp4')
# get_video_from_frames()
