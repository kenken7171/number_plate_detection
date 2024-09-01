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
    
    number_plate_image_list = []
    number_plate_image = data_generater.generate(2)
    number_plate_image = bright_changer.change(number_plate_image)
    number_plate_image = affinr_transformer.transform(number_plate_image)
    
    number_plate_image_list.append(number_plate_image)
    
    # number_plate_imageを保存
    # cv2.imwrite('output_image.jpg', number_plate_image)
    
    # ./data/backimage/samlpe.jpgを読み込み、number_plate_imageをsample.jpgに入れる
    back_image = cv2.imread('./data/backimage/sample.jpg')
    
    for number_plate_image in number_plate_image_list:
        image_widrh = number_plate_image.shape[1]
        image_height = number_plate_image.shape[0]
        left_coodinate_x = 0
        left_coodinate_y = 0
        
        back_image[0:220, 0:440] = number_plate_image
        cv2.imwrite('output_image.jpg', back_image)
    print("finish")