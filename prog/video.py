import cv2
import numpy as np
import glob

class Video:
    def __init__(self):
        pass

    def create_video_from_imgs(self, folder_path, out_name):
        img_array = []
        for filename in glob.glob(folder_path+'*.png'):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)
        out = cv2.VideoWriter(folder_path + out_name +'.avi',cv2.VideoWriter_fourcc(*'DIVX'), 10, size)
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
