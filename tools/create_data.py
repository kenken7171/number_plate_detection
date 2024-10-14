import os
import sys
import cv2
import glob
import random
import numpy as np
import argparse

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

MIN_BRIGHT_RATE = 0.5
MAX_BRIGHT_RATE = 1.0

def parse_args():
    parser = argparse.ArgumentParser(description='Create data')
    parser.add_argument('--make_data_num', type=int, default=MAKE_DATA_NUM, help='Make data number')
    parser.add_argument('--number_plate_num', type=int, default=NUMBER_PLATE_NUM, help='Number plate number')
    parser.add_argument('--min_size_rate', type=float, default=MIN_SIZE_RATE, help='Min size rate')
    parser.add_argument('--max_size_rate', type=float, default=MAX_SIZE_RATE, help='Max size rate')
    parser.add_argument('--min_bright_rate', type=float, default=MIN_BRIGHT_RATE, help='Min bright rate')
    parser.add_argument('--max_bright_rate', type=float, default=MAX_BRIGHT_RATE, help='Max bright rate')
    return parser.parse_args()

def set_parameter(args):
    global MAKE_DATA_NUM, NUMBER_PLATE_NUM, MIN_SIZE_RATE, MAX_SIZE_RATE, MIN_BRIGHT_RATE, MAX_BRIGHT_RATE
    MAKE_DATA_NUM = args.make_data_num
    NUMBER_PLATE_NUM = args.number_plate_num
    MIN_SIZE_RATE = args.min_size_rate
    MAX_SIZE_RATE = args.max_size_rate
    MIN_BRIGHT_RATE = args.min_bright_rate
    MAX_BRIGHT_RATE = args.max_bright_rate
    
def save_data(save_name,image,text):
    save_path = os.path.join(OUTPUT_PATH,save_name)
    cv2.imwrite(save_path + ".jpg", image)
    with open(save_path + ".txt", "w") as f:
        f.write(text)

class Back_Image:
    def __init__(self, back_image_path):
        self.back_image_list = glob.glob(back_image_path + "*.jpg")

    def get_back_image(self):
        back_image_path = random.choice(self.back_image_list)
        back_image = cv2.imread(back_image_path)
        return back_image


class Target_Image_util:
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
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    target_image_util = Target_Image_util(MIN_SIZE_RATE, MAX_SIZE_RATE)
    back_image_class = Back_Image(BACKIMAGE_PATH)
    number_plate_wrapper = Number_plate_wrapper()
    bright_changer = bc.BrightChanger(MIN_BRIGHT_RATE, MAX_BRIGHT_RATE)
    affine_transformer = at.AffineTransformer()
    for i in range(MAKE_DATA_NUM):
        print(f"make data {i+1}/{MAKE_DATA_NUM}")
        back_image = back_image_class.get_back_image()
        image_setter = iset.ImageSetter(back_image)
        for j in range(NUMBER_PLATE_NUM):
            number_plate_image, class_id = number_plate_wrapper.generate()
            number_plate_image = target_image_util.change_size(number_plate_image)
            number_plate_image = bright_changer.change(number_plate_image)
            number_plate_image = affine_transformer.transform(number_plate_image)
            composite_image = image_setter.set(number_plate_image, class_id)
        image_number = str(i).zfill(len(str(MAKE_DATA_NUM)))
        image_name = f"{image_number}"
        save_data(image_name,composite_image,image_setter.get_yolo_label())


if __name__ == "__main__":
    args = parse_args()
    set_parameter(args)
    main()
    print("finish")
