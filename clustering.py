from os import path, listdir, makedirs

import numpy as np
from cv2 import imread, VideoCapture, CAP_PROP_FPS, imwrite, VideoWriter, VideoWriter_fourcc, waitKey, calcHist
from sklearn.cluster import KMeans


class Clustering:
    def start(self, video, input_path, out_path, t, k, h):
        self.__get_frames_from_video(video, input_path)
        key_frames = self.__get_key_frames(input_path, t, k, h)
        self.__move_key_frames(input_path, out_path, key_frames)
        self.__get_video_from_frames(out_path)

    @staticmethod
    def __get_frames_from_video(video, input_path):
        if not path.exists(input_path):
            makedirs(input_path)
        video_cap = VideoCapture(video)
        success, image = video_cap.read()
        fps = int(video_cap.get(CAP_PROP_FPS))
        count = 0
        success = True
        while success:
            success, image = video_cap.read()
            imwrite(path.join(input_path, 'frame%05d.jpg' % count), image)
            count += 1

    @staticmethod
    def __move_key_frames(input_path, out_path, key_frames):
        if not path.exists(out_path):
            makedirs(out_path)
        for key_frame in key_frames:
            img_path = path.join(input_path, key_frame)
            imwrite(path.join(out_path, key_frame), imread(img_path))
            waitKey(0)

    @staticmethod
    def __get_video_from_frames(out_path):
        img = []
        for image in sorted(listdir(out_path)):
            img_path = path.join(out_path, image)
            img.append(imread(img_path))
        height, width, layers = img[1].shape
        avi = VideoWriter_fourcc(*'XVID')
        video = VideoWriter('resume.avi', avi, 1, (width, height))
        for i in img:
            video.write(i)

    @staticmethod
    def __get_key_frames(input_path, t, k, h):
        list_frames = {}
        aux = []
        n = len(listdir(input_path))
        f = 1
        for i, image in enumerate(sorted(listdir(input_path))):
            if f == 1 or (i == f and f <= n):
                img_path = path.join(input_path, image)
                img = imread(img_path)
                hist = calcHist([img.ravel()], [0], None, [256], h)
                hist_b = calcHist([img], [0], None, [256], [0, 256])
                hist_g = calcHist([img], [1], None, [256], [0, 256])
                hist_r = calcHist([img], [2], None, [256], [0, 256])
                # print(hist_b)
                for index in range(len(hist_r)):
                    m = (hist_b.item(index) + hist_g.item(index) + hist_r.item(index)) / 3.0
                    hist[index] = m
                ne = np.concatenate(list(hist))
                list_frames[image] = hist
                aux.append(list(ne))
                f += t
        print(len(aux))
        kmeans = KMeans(n_clusters=k, random_state=0).fit(aux)
        # print(kmeans.labels_)
        res = {i: np.where(kmeans.labels_ == i)[0] for i in range(kmeans.n_clusters)}
        # print(res) #GRUPO E INDICE DE LA FOTO
        res2 = {}
        for i, r in res.items():
            print("======================")
            print(len(r))
            print("======================")
            print("")

            aux2 = []
            for x in r:
                aux2.append(np.linalg.norm(aux[x] - kmeans.cluster_centers_[i]))
            res2[i] = aux2
        # print(res.items())
        ids = []
        for i, val in enumerate(res2.items()):
            print()
            print(val[1])
            print(len(val[1]))
            print(min(val[1]))
            print(val[1].index(min(val[1])))
            ids.append(val[1].index(min(val[1])))
            # print(sorted(val[1][1])[0])
        # print(len(ids))
        frames = []
        for i, r in enumerate(res.items()):
            print("*****************")
            print("ID: " + str(ids[i]) + " de " + str(len(r[1])))
            print(r[1][ids[i]])
            print(list(list_frames.keys())[r[1][ids[i]]])
            frames.append(list(list_frames.keys())[r[1][ids[i]]])
            print()
            # print(type(r[1]))
            # print(r[1][id])

        return frames
