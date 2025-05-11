from ultralytics import YOLO

def prediction(path_to_model="./trained_model/best.pt"):
    model = YOLO(path_to_model) # Can be replaced with other models
    result = model.predict(
        source="./test_images", # The folder where you put the pictures
        mode="predict",
    )

    return result



if __name__ == "__main__":
    prediction()
    # for r in result:
    #     boxes = r.boxes  # Boxes object for bounding box outputs
    #     masks = r.masks  # Masks object for segmentation masks outputs
    #     keypoints = r.keypoints  # Keypoints object for pose outputs
    #     probs = r.probs  # Probs object for classification outputs
    #     obb = r.obb  # Oriented boxes object for OBB outputs
    #     r.show()  # display to screen
    #     r.save(filename = "result.jpg")  # save to disk