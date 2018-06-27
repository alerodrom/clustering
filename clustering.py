from os import path, listdir

import numpy as np
from cv2 import imread, calcHist
from sklearn.cluster import KMeans

from frames import Frames
from util import timing


class Clustering:
    @timing
    def start(self, video, input_path, out_path, frames_video_path, t, k, h):
        """
        :param video: Ruta del vídeo
        :param input_path: Ruta donde se generarán los fotogramas del video
        :param out_path: Ruta donde se añadirán los fotogramas clave del video
        :param frames_video_path: Ruta donde se añadirán los fotogramas para generar el video resumen
        :param t: Número de fotogramas a saltar
        :param k: Número de grupos para k-means
        :param h: Tmañano del histográma generado
        """
        # Inicializamos la clase Frames
        frames = Frames()
        # Obtenemos los fotogramas del video
        # frames.get_frames_from_video(video, input_path)
        # Obtenemos fotogramas clave y fotogramas para generar el video
        key_frames, frames_video = self.__get_key_frames(input_path, t, k, h)
        # Movemos los fotogramas a sus respectivas carpetas
        frames.move_key_frames(input_path, out_path, key_frames)
        frames.move_key_frames(input_path, frames_video_path, frames_video)
        # Generamos el video resumen
        frames.get_video_from_frames(frames_video_path)

    @timing
    def __get_key_frames(self, input_path, t, k, h):
        """
        :param input_path: Ruta donde se generarán los fotogramas del video
        :param t: Número de fotogramas a saltar
        :param k: Número de grupos para k-means
        :param h: Tamaño del histográma generado
        :return: Devuelve los fotogramas clave y los fotogramas para generar el video resumen
        """
        # Diccionario que almacenará como clave el nombre del fotograma y el valor del histograma
        list_frames = {}
        # Lista con el valor de todos los histogramas
        hist_all = []
        # Número de fotogramas
        n = len(listdir(input_path))
        f = 1
        # Recorremos los fotogramas ordenados
        for i, image in enumerate(sorted(listdir(input_path))):
            # Comprobamos que se cumple
            if f == 1 or (i == f and f <= n):
                img_path = path.join(input_path, image)
                img = imread(img_path)
                # Calculamos la media del histograma de los tres colores
                hist = self.__hist_average(img, h)
                ne = np.concatenate(list(hist))
                # Actualizamos el diccionario
                list_frames[image] = hist
                # Actualizamos la lista de histogramas
                hist_all.append(list(ne))
                f += t
        kmeans = KMeans(n_clusters=k, random_state=0).fit(hist_all)
        # Obtenemos los indices de hist_all por cada grupo (cluster) de kmeans
        res = {i: np.where(kmeans.labels_ == i)[0] for i in range(kmeans.n_clusters)}
        # Obtenemos las distancias del cluster
        distances_cluster = self.__get_distance(res, kmeans, hist_all)
        # Obtenemos los indices de las menores distancias de cada grupo (cluster)
        ids = self.__get_min(distances_cluster)

        return self.__get_frames_near(res, ids, list_frames)

    @staticmethod
    def __hist_average(img, h):
        """
        :param img: Imagen cargada
        :param h: Tamaño del histográma generado
        :return: Devuelve la media de los histogramas R, G y B
        """
        # Iniciamos
        hist = calcHist([img.ravel()], [0], None, [256], h)
        # Calculamos los histogramas por cada color
        hist_b = calcHist([img], [0], None, [256], h)
        hist_g = calcHist([img], [1], None, [256], h)
        hist_r = calcHist([img], [2], None, [256], h)
        # Calculamos la media de los histogramas
        for index in range(len(hist_r)):
            hist[index] = (hist_b.item(index) + hist_g.item(index) + hist_r.item(index)) / 3.0
        return hist

    @staticmethod
    def __get_distance(values, kmeans, hist_all):
        """
        :param values: Diccionario que almacena como clave el cluster y como valor el indice que tiene en hist_all
        :param kmeans: K medias
        :param hist_all: Listado con el valor de los histogramas
        :return: Devuelve un diccionario, para cada cluster almacena las distancias
        """
        res = {}
        # Para cada cluster
        for i, r in values.items():
            aux = []
            # Obtenemos el id al que hace referencia en hist_all
            for x in r:
                # Calculamnos la distancia normal entre el histograma y el centroide del cluster
                aux.append(np.linalg.norm(hist_all[x] - kmeans.cluster_centers_[i]))
            res[i] = aux
        return res

    @staticmethod
    def __get_min(distances_cluster):
        """
        :param distances_cluster: Distancias del cluster
        :return: Devolvemos los ids
        """
        ids = []
        # Recorremos los items del diccionario
        for i, val in enumerate(distances_cluster.items()):
            # Obtenemos indice del que tiene menor valor
            ids.append(val[1].index(min(val[1])))
        return ids

    @staticmethod
    def __get_frames_near(res, ids, list_frames):
        """
        :param res: Diccionario que almacena como clave el cluster y como valor el indice que tiene en hist_all
        :param ids: Id que hace referencia al item de res
        :param list_frames: Diccionario que almacena como clave el nombre del fotograma y el valor del histograma
        :return: Devolvemos el listado de fotogramas clave y fotogramas para generar el video resumen
        """
        frames_video = []
        key_frames = []
        items = sorted(listdir('input'))
        # Recorremos cada cluster
        for i, r in enumerate(res.items()):
            # Obtenemos el fotograma clave
            key_frames.append(list(list_frames.keys())[r[1][ids[i]]])
            aux = []
            # Obtenemos el indice del fotograma clave
            id_frame = items.index(list(list_frames.keys())[r[1][ids[i]]])
            # Obtenemos 4 veces el tamaño del cluster más uno por la izquierda y derecha del fotograma
            aux.extend(items[id_frame - 2 * (2 * len(r[1])) + 1: id_frame])
            aux.extend(items[id_frame: id_frame + 2 * (2 * len(r[1])) + 1])
            frames_video.extend(aux)

        return key_frames, frames_video
