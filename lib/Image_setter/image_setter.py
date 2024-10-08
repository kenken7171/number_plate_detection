import cv2
import numpy as np
import random
from PIL import Image


class Conflict_checker:
    def __init__(self, multiplicity_rate):
        self.__multiplicity_rate = multiplicity_rate

    def check(self, rect, rect_list):
        conflict = False
        for r in rect_list:
            iou = self.__multiplicity(r, rect)
            if iou > self.__multiplicity_rate:
                conflict = True
                break
        if not conflict:
            return True
        return False

    def __multiplicity(self, rect1, rect2):
        (ax_mn, ay_mn) = rect1[0]
        (ax_mx, ay_mx) = rect1[1]
        (bx_mn, by_mn) = rect2[0]
        (bx_mx, by_mx) = rect2[1]
        a_area = (ax_mx - ax_mn + 1) * (ay_mx - ay_mn + 1)
        b_area = (bx_mx - bx_mn + 1) * (by_mx - by_mn + 1)
        abx_mn = max(ax_mn, bx_mn)
        aby_mn = max(ay_mn, by_mn)
        abx_mx = min(ax_mx, bx_mx)
        aby_mx = min(ay_mx, by_mx)
        w = max(0, abx_mx - abx_mn + 1)
        h = max(0, aby_mx - aby_mn + 1)
        intersect = w * h
        return intersect / (a_area + b_area - intersect)


class ImageSetter:
    def __init__(self, back_image, multiplicity_rate=0):
        self.composite_image = back_image
        self.composite_image = cv2.cvtColor(self.composite_image, cv2.COLOR_BGR2BGRA)
        self.height = back_image.shape[0]
        self.width = back_image.shape[1]
        self.conflict_checker = Conflict_checker(multiplicity_rate)
        self.rect_list = []
        self.class_id_list = []

    def set(self, target_image, class_id):
        rect = self.__get_random_position(target_image)
        is_conflict = self.conflict_checker.check(rect, self.rect_list)
        if is_conflict:
            self.rect_list.append(rect)
            self.class_id_list.append(class_id)
            self.composite_image = self.__make_composite_image(target_image, rect)
        return self.composite_image

    def __get_random_position(self, target_image):
        target_height = target_image.shape[0]
        target_width = target_image.shape[1]
        x = random.randint(0, self.width - target_width)
        y = random.randint(0, self.height - target_height)
        return (x, y), (x + target_width, y + target_height)

    def __make_composite_image(self, target_image, rect):
        # target_imageのアルファチェンネルがない場合、アルファチャンネルを追加
        if len(target_image.shape) == 3:
            target_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2BGRA)
        # target_imageのアルファチャンネルが0の場合はtarget_imageを貼り付ける。
        # それ以外はself.composite_imageを貼り付ける。
        (x_mn, y_mn), (x_mx, y_mx) = rect
        for y in range(y_mn, y_mx):
            for x in range(x_mn, x_mx):
                if target_image[y - y_mn, x - x_mn, 3:] != 0:
                    self.composite_image[y, x] = target_image[y - y_mn, x - x_mn]
        return self.composite_image

    def make_yolo_label(self):
        label = ""
        for i in range(len(self.rect_list)):
            (x_mn, y_mn), (x_mx, y_mx) = self.rect_list[i]
            x = (x_mn + x_mx) / 2 / self.width
            y = (y_mn + y_mx) / 2 / self.height
            w = (x_mx - x_mn) / self.width
            h = (y_mx - y_mn) / self.height
            label += f"{self.class_id_list[i]} {x} {y} {w} {h}\n"
        return label

    def get_yolo_label(self):
        return self.make_yolo_label()


if __name__ == "__main__":
    # 例:
    # 背景画像の読み込み
    bg_image = cv2.imread("sample.jpg")
    # 挿入したい画像の読み込み
    fg_image = cv2.imread("plate_image.jpg")
    image_setter = ImageSetter()
    image_setter.init_image(bg_image.shape[1], bg_image.shape[0])
    # 背景画像に挿入したい画像を挿入
    result_image = image_setter.random_image_setter(
        bg_image, fg_image, [0.0, 0.2], [0.5, 1.0]
    )

    # 挿入後の画像を保存
    cv2.imwrite("output_image.jpg", result_image)

    print("finish")
