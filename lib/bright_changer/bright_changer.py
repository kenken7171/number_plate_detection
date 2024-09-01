import cv2
import numpy as np
import random


class BrightChanger:
    def __init__(self):
        self.bright_rate = self.get_random_rate()

    def get_random_rate(self):
        # 0.1 ~ 1.0の範囲でランダムな明るさを設定
        return random.uniform(0.1, 1.0)

    def change(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = np.clip(v * self.bright_rate, 0, 255).astype(np.uint8)
        hsv = cv2.merge((h, s, v))
        image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        # 背景を透過させるために、全てのピクセルの値に+1をする
        image = image + 1
        return image
