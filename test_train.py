from ultralytics import YOLO


if __name__ == "__main__":
        
    # Load a model
    model = YOLO("yolo11n.pt")  # load a pretrained model (recommended for training)

    results = model.train(data="./dataset/data.yaml", epochs=100, imgsz=640)
