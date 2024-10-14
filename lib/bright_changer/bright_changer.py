import cv2
import numpy as np
import random


class BrightChanger:
    def __init__(self,min_rate=0.5,max_rate=1.0):
        self.min_rate = min_rate
        self.max_rate = max_rate
        self.bright_rate = 1.0

    def get_random_rate(self):
        # 0.5 ~ 1.0の範囲でランダムな明るさを設定
        return random.uniform(self.min_rate, self.max_rate)

    def change(self, image):
        self.bright_rate = self.get_random_rate()
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = np.clip(v * self.bright_rate, 0, 255).astype(np.uint8)
        hsv = cv2.merge((h, s, v))
        image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return image
