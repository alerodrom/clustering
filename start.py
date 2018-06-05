from clustering import Clustering

my_clustering = Clustering()

my_clustering.start('media/video.mp4', 'input', 'output', 'frames_videos', 100, 15, [0, 256])

# 100, 20
# 100, 15, [0, 256] 0.530 s
# 100, 8, [0, 256] 0.421 s
# 100, 8, [0, 256] 0.381 s
