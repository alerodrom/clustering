from os import path, listdir, makedirs

from cv2 import imread, VideoCapture, imwrite, VideoWriter, VideoWriter_fourcc, waitKey


class Frames:
    @staticmethod
    def get_frames_from_video(video, input_path):
        """
        :param video: Ruta del vídeo
        :param input_path: Ruta donde se generarán los fotogramas del video
        """
        # Si no existe la ruta la creamos
        if not path.exists(input_path):
            makedirs(input_path)
        # Cargamos el video
        video_cap = VideoCapture(video)
        success, image = video_cap.read()
        count = 0
        success = True
        # Guardamos los fotogramas
        while success:
            success, image = video_cap.read()
            imwrite(path.join(input_path, 'frame%05d.jpg' % count), image)
            count += 1

    @staticmethod
    def move_key_frames(input_path, out_path, key_frames):
        """
        :param input_path: Ruta donde se generarán los fotogramas del video
        :param out_path: Ruta donde se moveran los fotogramas del video
        :param key_frames: Fotogramas claves
        """
        if not path.exists(out_path):
            makedirs(out_path)
        # Recorremos los fotogramas clave y los movemos a la carpeta deseada
        for key_frame in key_frames:
            img_path = path.join(input_path, key_frame)
            imwrite(path.join(out_path, key_frame), imread(img_path))
            waitKey(0)

    @staticmethod
    def get_video_from_frames(out_path):
        """
        :param out_path: Ruta donde se añadirán los fotogramas clave del video
        """
        img = []
        # Recorremos las imagenes que tenga out_path y cargamos la imagen
        for image in sorted(listdir(out_path)):
            img_path = path.join(out_path, image)
            img.append(imread(img_path))
        # Tamaño del marco del video
        height, width, layers = img[1].shape
        # Formato
        avi = VideoWriter_fourcc(*'XVID')
        # Inicializamos el video y añadimos los fotogramas
        video = VideoWriter('resume.avi', avi, 21, (width, height))
        for i in img:
            video.write(i)
