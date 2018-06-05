from os import path, listdir

import numpy as np
from cv2 import imread, calcHist
from sklearn.cluster import KMeans

from frames import Frames
from util import timing


class Clustering:
    @timing
    def start(self, video, input_path, out_path, frames_video_path, t, k, h):
        frames = Frames()
        frames.get_frames_from_video(video, input_path)
        key_frames, frames_video = self.__get_key_frames(input_path, t, k, h)
        frames.move_key_frames(input_path, out_path, key_frames)
        frames.move_key_frames(input_path, frames_video_path, frames_video)
        frames.get_video_from_frames(frames_video_path)

    @timing
    def __get_key_frames(self, input_path, t, k, h):
        list_frames = {}
        hist_all = []
        n = len(listdir(input_path))
        f = 1
        for i, image in enumerate(sorted(listdir(input_path))):
            if f == 1 or (i == f and f <= n):
                img_path = path.join(input_path, image)
                img = imread(img_path)
                hist = self.__hist_average(img, h)
                ne = np.concatenate(list(hist))
                list_frames[image] = hist
                hist_all.append(list(ne))
                f += t
        print(len(hist_all))
        kmeans = KMeans(n_clusters=k, random_state=0).fit(hist_all)
        res = {i: np.where(kmeans.labels_ == i)[0] for i in range(kmeans.n_clusters)}
        distances_cluster = self.__get_distance(res, kmeans, hist_all)
        ids = self.__get_min(distances_cluster)

        return self.__get_frames_near(res, ids, list_frames)

    @staticmethod
    def __hist_average(img, h):
        hist = calcHist([img.ravel()], [0], None, [256], h)
        hist_b = calcHist([img], [0], None, [256], h)
        hist_g = calcHist([img], [1], None, [256], h)
        hist_r = calcHist([img], [2], None, [256], h)
        for index in range(len(hist_r)):
            hist[index] = (hist_b.item(index) + hist_g.item(index) + hist_r.item(index)) / 3.0
        return hist

    @staticmethod
    def __get_distance(values, kmeans, hist_all):
        res = {}
        for i, r in values.items():
            print("======================")
            print(len(r))
            print("======================")
            print("")

            aux = []
            for x in r:
                aux.append(np.linalg.norm(hist_all[x] - kmeans.cluster_centers_[i]))
            res[i] = aux
        return res

    @staticmethod
    def __get_min(distances_cluster):
        ids = []
        for i, val in enumerate(distances_cluster.items()):
            print()
            print(val[1])
            print(len(val[1]))
            print(min(val[1]))
            print(val[1].index(min(val[1])))
            ids.append(val[1].index(min(val[1])))
        return ids

    @staticmethod
    def __get_frames_near(res, ids, list_frames):
        frames_video = []
        key_frames = []
        for i, r in enumerate(res.items()):
            aux = []
            print("*****************")
            print("ID: " + str(ids[i]) + " de " + str(len(r[1])))
            id_frame = sorted(listdir('input')).index(list(list_frames.keys())[r[1][ids[i]]])
            print(id_frame)
            print("IZQ =" + str(sorted(listdir('input'))[id_frame - 10: id_frame]))
            print(sorted(listdir('input'))[id_frame])
            print("DER =" + str(sorted(listdir('input'))[id_frame + 1: id_frame + 11]))
            aux.extend(sorted(listdir('input'))[id_frame - 10: id_frame])
            aux.append(list(list_frames.keys())[r[1][ids[i]]])
            aux.extend(sorted(listdir('input'))[id_frame + 1: id_frame + 11])
            frames_video.extend(aux)
            key_frames.append(list(list_frames.keys())[r[1][ids[i]]])
        return key_frames, frames_video
