import cv2
import numpy as np
import random

class BrightChanger:
    def __init__(self):
        self.bright_rate = 0.5
        
    def set_random_rate(self):
        # 0 ~ 1.0の範囲でランダムな明るさを設定
        self.bright_rate = random.random()

    def change(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = np.clip(v * self.bright_rate, 0, 255).astype(np.uint8)
        hsv = cv2.merge((h, s, v))
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)