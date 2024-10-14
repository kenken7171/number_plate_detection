import os

os.makedirs("./data", exist_ok=True)
os.makedirs("./data/backimage", exist_ok=True)
os.makedirs("./data/output", exist_ok=True)
os.makedirs("./data/yolo", exist_ok=True)

os.makedirs("./data/yolo/train", exist_ok=True)
os.makedirs("./data/yolo/train/images", exist_ok=True)
os.makedirs("./data/yolo/train/labels", exist_ok=True)
os.makedirs("./data/yolo/val", exist_ok=True)
os.makedirs("./data/yolo/val/images", exist_ok=True)
os.makedirs("./data/yolo/val/labels", exist_ok=True)
os.makedirs("./data/yolo/test", exist_ok=True)
os.makedirs("./data/yolo/test/images", exist_ok=True)
os.makedirs("./data/yolo/test/labels", exist_ok=True)
