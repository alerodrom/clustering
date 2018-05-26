from os import path, listdir, makedirs

from cv2 import imread, VideoCapture, CAP_PROP_FPS, imwrite, VideoWriter, VideoWriter_fourcc, waitKey


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
        cont_aux = 0
        while success:
            success, image = video_cap.read()
            if count % fps == 0:
                cont_aux += 1
                imwrite(path.join(input_path, 'frame%03d.jpg' % cont_aux), image)
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
        # list_frames = {}
        n = len(listdir(input_path))
        f = 1
        list_frames = []
        for image in sorted(listdir(input_path)):
            if f == 1 or f <= n:
                list_frames.append(image)
                f += t
        return list_frames

    @staticmethod
    def __k_medias(list_frames, k):
        pass

    @staticmethod
    def __calculate_centroid_classes(list_frames_classified, k):
        pass
