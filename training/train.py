from ultralytics import YOLO

model = YOLO("yolov8s.pt")

model.train(
    data="data.yaml",
    epochs=50,
    imgsz=640,
    batch=16,
    workers=4,
    cache=True,
    save=True,
    save_period=1,
    project="FoodAI_v2",
    name="Balanced80"
)