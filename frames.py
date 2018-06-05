from os import path, listdir, makedirs

from cv2 import imread, VideoCapture, imwrite, VideoWriter, VideoWriter_fourcc, waitKey


class Frames:
    @staticmethod
    def get_frames_from_video(video, input_path):
        if not path.exists(input_path):
            makedirs(input_path)
        video_cap = VideoCapture(video)
        success, image = video_cap.read()
        count = 0
        success = True
        while success:
            success, image = video_cap.read()
            imwrite(path.join(input_path, 'frame%05d.jpg' % count), image)
            count += 1

    @staticmethod
    def move_key_frames(input_path, out_path, key_frames):
        if not path.exists(out_path):
            makedirs(out_path)
        for key_frame in key_frames:
            img_path = path.join(input_path, key_frame)
            imwrite(path.join(out_path, key_frame), imread(img_path))
            waitKey(0)

    @staticmethod
    def get_video_from_frames(out_path):
        img = []
        for image in sorted(listdir(out_path)):
            img_path = path.join(out_path, image)
            img.append(imread(img_path))
        height, width, layers = img[1].shape
        avi = VideoWriter_fourcc(*'XVID')
        video = VideoWriter('resume.avi', avi, 21, (width, height))
        for i in img:
            video.write(i)
