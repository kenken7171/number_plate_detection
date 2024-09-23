import cv2
import numpy as np
import argparse
import random


class AffineTransformer:

    def affine_transform(self, image, src_points, dst_points):
        """
        画像を台形にアフィン変換する関数

        Parameters:
        image (numpy.ndarray): 入力画像
        src_points (list): 元画像の四隅の座標 [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        dst_points (list): 変換後の台形の四隅の座標 [(x1', y1'), (x2', y2'), (x3', y3'), (x4', y4')]

        Returns:
        numpy.ndarray: 台形に変換された画像
        """

        # 入力ポイントと出力ポイントをnumpy配列に変換
        src_pts = np.float32(src_points)
        dst_pts = np.float32(dst_points)

        # 変換行列を取得
        matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)

        # 画像サイズ（幅と高さ）
        h, w = image.shape[:2]

        # 変換後の画像を生成、余白は黒で埋める
        transformed_image = cv2.warpPerspective(
            image, matrix, (w, h), borderValue=(255, 255, 255)
        )
        return transformed_image

    def transform(self, image):
        height = image.shape[0]
        width = image.shape[1]
        src_points = [
            (0, 0),
            (image.shape[1], 0),
            (image.shape[1], image.shape[0]),
            (0, image.shape[0]),
        ]
        # 4辺のどれかを短くするために、0から3のランダムな数を取得（0：上辺、1：右辺、2：下辺、3：左辺）
        short_side = random.randint(0, 3)
        trans_raito = 0.95
        cut_width = int(width * (1 - trans_raito))
        cut_height = int(height * (1 - trans_raito))
        dst_points = []
        if short_side == 0:
            # 上辺をtrans_raito倍にする
            dst_points = [
                (cut_width, 0),
                (image.shape[1] - cut_width, 0),
                (image.shape[1], image.shape[0]),
                (0, image.shape[0]),
            ]
        elif short_side == 1:
            # 右辺をtrans_raito倍にする
            dst_points = [
                (0, 0),
                (image.shape[1], cut_height),
                (image.shape[1], image.shape[0] - cut_height),
                (0, image.shape[0]),
            ]
        elif short_side == 2:
            # 下辺をtrans_raito倍にする
            dst_points = [
                (0, 0),
                (image.shape[1], 0),
                (image.shape[1] - cut_width, image.shape[0]),
                (cut_width, image.shape[0]),
            ]
        elif short_side == 3:
            # 左辺をtrans_raito倍にする
            dst_points = [
                (0, cut_height),
                (image.shape[1], 0),
                (image.shape[1], image.shape[0]),
                (0, image.shape[0] - cut_height),
            ]
        return self.affine_transform(image, src_points, dst_points)


if __name__ == "__main__":
    # 例:
    # 入力画像の読み込み
    image = cv2.imread("sample.jpg")
    # print(image.shape)
    affine_transfer = AffineTransformer()
    # 画像を変換
    transformed_image = affine_transfer.transform(image)

    # 変換後の画像を保存
    cv2.imwrite("output_image.jpg", transformed_image)

    # 元画像の四隅の座標
    # src_points = [(0, 0), (image.shape[1], 0), (image.shape[1], image.shape[0]), (0, image.shape[0])]

    # 変換後の台形の四隅の座標 (例として、上部を縮めて台形にする)
    # dst_points = [(100, 0), (image.shape[1] - 100, 0), (image.shape[1], image.shape[0]), (0, image.shape[0])]
