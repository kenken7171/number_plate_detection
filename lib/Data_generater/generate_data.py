from number_plate import NumberPlate
from PIL import Image, ImageDraw, ImageFont

category=0 # 0:普通車（自家用） 1:普通車（事業用） 2:軽自動車（自家用） 3:軽自動車（事業用）
n_category_data = [4000,1000,4000,1000]

number_plate = NumberPlate()

for n_category in range(len(n_category_data)):
    print(f"category: {n_category}")
    for i in range(n_category_data[n_category]):
        print(f"category: {n_category}, i: {i}")
        img_np = number_plate.generate(n_category)
        im = Image.fromarray(img_np)
        filename = str(i).zfill(len(str(n_category_data[n_category])))
        im.save(f"../../data/{str(n_category)}/{filename}.jpeg" )

# img_np = number_plate.generate(category)
# # print(type(img))

# im = Image.fromarray(img_np)
# im.save("filename.jpeg")

class DataGenerater:
    def __init__(self):
        self.number_plate = NumberPlate()
    
    def generate(self, category, n_category_data):
        for n_category in range(len(n_category_data)):
            print(f"category: {n_category}")
            for i in range(n_category_data[n_category]):
                print(f"category: {n_category}, i: {i}")
                img_np = self.number_plate.generate(n_category)
                im = Image.fromarray(img_np)
                filename = str(i).zfill(len(str(n_category_data[n_category])))
                im.save(f"../../data/{str(n_category)}/{filename}.jpeg" )