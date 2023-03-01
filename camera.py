import threading

import cv2
import numpy as np


class Camera (object):
    def __init__(self, camera_url):
        self.camera_url = camera_url
        self.frame = np.empty(3)
        self.stop = False

        self.thread = threading.Thread(target=self.start, daemon=True)
        self.thread.start()

    def start(self):
        cap = cv2.VideoCapture(self.camera_url if self.camera_url != '0' else 0)

        if cap.isOpened():
            while not self.stop:
                ret, frame = cap.read()

                if ret:
                    self.frame = frame

        cap.release()

    def get_frame(self):
        return self.frame.copy()

    def stop_camera(self):
        self.stop = True
        self.thread.join()

