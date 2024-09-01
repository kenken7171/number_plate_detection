import cv2
import numpy as np
import random


class ImageSetter:
    def __init__(self):
        self.image = None
        self.random_try_count = 5

    def init_image(self, image_width, image_height):
        """
        画像を初期化する

        Args:
        image_width (int): 画像の幅
        image_height (int): 画像の高さ

        Returns:
        numpy.ndarray: 初期化された画像
        """
        # 画像を初期化
        self.image = np.zeros((image_height, image_width, 3), np.uint8)

    # 画像の透過処理を行う関数。黒を透過する。
    def transparent_processing(self, image):
        """
        画像の透過処理を行う

        Args:
        image (numpy.ndarray): 透過処理を行う画像

        Returns:
        numpy.ndarray: 透過処理後の画像
        """
        # 画像の高さと幅
        height, width = image.shape[:2]

        # 黒色部分に対応するマスク画像を生成
        mask = np.all(image == [0, 0, 0], axis=2)

        # 元画像をBGR形式からBGRA形式に変換
        dst = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

        # マスク画像をもとに、黒色部分を透明化
        dst[:, :, 3] = np.where(mask, 0, 255)

        # BGRA形式からBGR形式に変換
        image = cv2.cvtColor(dst, cv2.COLOR_BGRA2BGR)

        return image

    # 背景の画像に挿入したい画像を挿入する関数
    # bg_image: 背景の画像
    # fg_image: 挿入したい画像
    def set_image(self, bg_image, fg_image, x, y):
        """
        背景の画像に挿入したい画像を挿入する

        Args:
        bg_image (numpy.ndarray): 背景の画像
        fg_image (numpy.ndarray): 挿入したい画像
        x (int): 挿入するx座標
        y (int): 挿入するy座標

        Returns:
        numpy.ndarray: 挿入後の画像
        """
        # 背景画像の高さと幅
        bg_height, bg_width = bg_image.shape[:2]

        # 挿入したい画像の高さと幅
        fg_height, fg_width = fg_image.shape[:2]

        # 挿入したい画像の範囲が背景画像の範囲を超えていないか確認
        if x + fg_width > bg_width or y + fg_height > bg_height:
            raise ValueError("挿入したい画像が背景画像の範囲を超えています")

        # 挿入したい画像の透過処理
        fg_image = self.transparent_processing(fg_image)

        # 背景画像に挿入したい画像を挿入
        bg_image[y : y + fg_height, x : x + fg_width] = fg_image

        return bg_image

    # range_widthの範囲内でself.imageの値が0でない場合にbg_imageにfg_imageを挿入する関数。
    # もしself.imageの値が0でない場合には、self.random_try_count回繰り返す。
    # それでもself.imageの値が0でない場合には、Falseを返す。
    def random_image_setter(self, bg_image, fg_image, range_width, range_height):
        """
        range_widthの範囲内でself.imageの値が0でない場合にbg_imageにfg_imageを挿入する。
        もしself.imageの値が0でない場合には、self.random_try_count回繰り返す。
        それでもself.imageの値が0でない場合には、Falseを返す。

        Args:
        bg_image (numpy.ndarray): 背景の画像
        fg_image (numpy.ndarray): 挿入したい画像
        range_width (list[float]): 挿入するx座標の範囲、値としては0から1の範囲
        range_height (list[float]): 挿入するy座標の範囲、値としては0から1の範囲

        Returns:
        numpy.ndarray: 挿入後の画像
        """
        # 背景画像の高さと幅
        bg_height, bg_width = bg_image.shape[:2]

        # 挿入したい画像の高さと幅
        fg_height, fg_width = fg_image.shape[:2]

        # 挿入したい画像の透過処理
        fg_image = self.transparent_processing(fg_image)

        # 挿入するx座標の範囲
        x_range = (int(bg_width * range_width[0]), int(bg_width * range_width[1]))

        # 挿入するy座標の範囲
        y_range = (int(bg_height * range_height[0]), int(bg_height * range_height[1]))

        while_count = 0
        while while_count <= self.random_try_count:
            # 挿入するx座標とy座標
            x = random.randint(x_range[0], x_range[1])
            y = random.randint(y_range[0], y_range[1])
            # 挿入したい画像の範囲が背景画像の範囲を超えていないか確認
            if x + fg_width > bg_width or y + fg_height > bg_height:
                continue
            # 挿入する範囲のself.imageの値が0であるか確認
            if np.all(self.image[y : y + fg_height, x : x + fg_width] == 0):
                # 挿入したい画像を挿入
                return self.set_image(bg_image, fg_image, x, y)
            while_count += 1

        return False


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
