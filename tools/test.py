import os
import sys
import cv2
sys.path.append(os.path.join(os.path.dirname(__file__), '../lib'))
from Data_generater import number_plate as dg
from Bright_changer import bright_changer as bc
from Affine_transformer import affine_transformer as at

if __name__ == "__main__":
    data_generater = dg.NumberPlate()
    bright_changer = bc.BrightChanger()
    affinr_transformer = at.AffineTransformer()
    
    number_plate_image = data_generater.generate(0)
    number_plate_image = bright_changer.change(number_plate_image)
    number_plate_image = affinr_transformer.transform(number_plate_image)
    # number_plate_imageを保存
    cv2.imwrite('output_image.jpg', number_plate_image)
    print("finish")