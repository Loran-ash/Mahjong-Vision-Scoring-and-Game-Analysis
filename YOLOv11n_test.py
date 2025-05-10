from ultralytics import YOLO


if __name__ == "__main__":
        
    # Load a model
    model = YOLO("yolo11n.pt")  # load a pretrained model (recommended for training)

    # Train the model
    results = model.train(data="coco8.yaml", epochs=100, imgsz=640) #COCO8是個小資料集，執行時會自動幫你下載，可以自己跑跑看他的效果如何