import os
import sys
import cv2
import glob
import random
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))
from Data_generater import number_plate as dg
from Bright_changer import bright_changer as bc
from Affine_transformer import affine_transformer as at
from Image_setter import image_setter as iset

BACKIMAGE_PATH = "./data/backimage/"
OUTPUT_PATH = "./data/output/"

MAKE_DATA_NUM = 1

# 1枚あたりのナンバープレートの数
NUMBER_PLATE_NUM = 5

# 画像のサイズの縮尺
MIN_SIZE_RATE = 0.5
MAX_SIZE_RATE = 1.5


class Back_Image:
    def __init__(self, back_image_path):
        self.back_image_list = glob.glob(back_image_path + "*.jpg")

    def get_back_image(self):
        back_image_path = random.choice(self.back_image_list)
        back_image = cv2.imread(back_image_path)
        return back_image


class Tarqet_Image_util:
    def __init__(self, min_size_rate, max_size_rate):
        self.min_size_rate = min_size_rate
        self.max_size_rate = max_size_rate

    def change_size(self, image):
        height, width = image.shape[:2]
        size_rate = random.uniform(self.min_size_rate, self.max_size_rate)
        image = cv2.resize(image, (int(width * size_rate), int(height * size_rate)))
        return image


class Number_plate_wrapper:
    def __init__(self):
        self.number_plate = dg.NumberPlate()

    def generate(self, class_id=None):
        if class_id is None:
            class_id = random.randint(0, self.number_plate.get_max_category_length())
        number_plate_image = self.number_plate.generate(class_id)
        number_plate_image = self.__transparent(number_plate_image)
        return number_plate_image, class_id

    def __transparent(self, image):
        mask = np.all(image[:, :, :] == [255, 255, 255], axis=-1)
        # Point 2: 元画像をBGR形式からBGRA形式に変換
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        # Point3: マスク画像をもとに、白色部分を透明化
        image[mask, 3] = 0
        return image


def main():
    print("main")
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    target_image_util = Tarqet_Image_util(MIN_SIZE_RATE, MAX_SIZE_RATE)
    back_image_class = Back_Image(BACKIMAGE_PATH)
    number_plate_wrapper = Number_plate_wrapper()
    bright_changer = bc.BrightChanger()
    affine_transformer = at.AffineTransformer()
    for i in range(MAKE_DATA_NUM):
        back_image = back_image_class.get_back_image()
        image_setter = iset.ImageSetter(back_image)
        for j in range(NUMBER_PLATE_NUM):
            number_plate_image, class_id = number_plate_wrapper.generate()
            number_plate_image = target_image_util.change_size(number_plate_image)
            number_plate_image = bright_changer.change(number_plate_image)
            number_plate_image = affine_transformer.transform(number_plate_image)
            composite_image = image_setter.append(number_plate_image, class_id)
            cv2.imwrite(OUTPUT_PATH + f"output_{i}.jpg", composite_image)


if __name__ == "__main__":
    # data_generater = dg.NumberPlate()
    # bright_changer = bc.BrightChanger()
    # affinr_transformer = at.AffineTransformer()

    # number_plate_image_list = []
    # number_plate_image = data_generater.generate(2)
    # number_plate_image = bright_changer.change(number_plate_image)
    # number_plate_image = affinr_transformer.transform(number_plate_image)

    # number_plate_image_list.append(number_plate_image)

    # # number_plate_imageを保存
    # cv2.imwrite("plate_image.jpg", number_plate_image)

    # # ./data/backimage/samlpe.jpgを読み込み、number_plate_imageをsample.jpgに入れる
    # back_image = cv2.imread("./data/backimage/sample.jpg")

    # for number_plate_image in number_plate_image_list:
    #     image_widrh = number_plate_image.shape[1]
    #     image_height = number_plate_image.shape[0]
    #     left_coodinate_x = 0
    #     left_coodinate_y = 0

    #     back_image[0:220, 0:440] = number_plate_image
    #     cv2.imwrite("output_image.jpg", back_image)
    main()
    print("finish")
