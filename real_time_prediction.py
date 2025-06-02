import cv2
from ultralytics import YOLO
from gradio_webrtc import WebRTC
import math
import time
from yolo_classify import convert_label
import requests


model = YOLO("./trained_model/best.pt")
# model = YOLO("yolo11n.pt")
classNames = ["circle_1", "circle_2", "circle_3", "circle_4", "circle_5", "circle_6", "circle_7", "circle_8", "circle_9",
            "bamboo_1", "bamboo_2", "bamboo_3", "bamboo_4", "bamboo_5", "bamboo_6", "bamboo_7", "bamboo_8", "bamboo_9",
            "character_1", "character_2", "character_3", "character_4", "character_5", "character_6", "character_7", "character_8", "character_9",
            "north", "south", "west", "east", "green", "red", "white" ]

# classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
#             "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
#             "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
#             "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
#             "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
#             "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
#             "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
#             "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
#             "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
#             "teddy bear", "hair drier", "toothbrush"
#             ]

def real_time_predict(cap=cv2.VideoCapture(1)):

    #cap = cv2.VideoCapture(0)
    # cap.set(3, 640)
    # cap.set(4, 480)

    #while True:
    ret, img = cap.read()
    results = model(img, stream=True)
    tile_labels = []
    
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            tile_labels.append(convert_label(label))

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)

            # class name
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            #cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
    #cv2.imshow('Webcam', img)  #不想顯示畫面，可以註解掉這行

    if cv2.waitKey(1) == ord('q'):
        return

    # cap.release()
    # cv2.destroyAllWindows()
    return img, ", ".join(tile_labels)

def detection(image, last_result):
    image = cv2.resize(image, (720, 480)) #之所以size這麼小是因為電腦效能的原因
    try:
        result = model.predict(image)
        if len(result) == 0 or len(result[0].boxes) == 0:
            return image, last_result
        tile_labels = []

        for r in result:
            if hasattr(r, "boxes") and r.boxes:
                for box in r.boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                    # put box in cam
                    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    cls_id = int(box.cls[0])
                    label = model.names[cls_id]
                    tile_labels.append(convert_label(label))
                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    color = (255, 0, 0)
                    thickness = 2
                    cls = int(box.cls[0])
                    cv2.putText(image, classNames[cls], org, font, fontScale, color, thickness)

        #if len(tile_labels) != 17:
        #    return f"⚠️ 檢測牌數錯誤（辨識到 {len(tile_labels)} 張）: {tile_labels}"

        #return ", ".join(tile_labels)
        #image = draw_boxes(result, image)
        #pred_text = "testtest"
    except Exception as e:
        return image, str(e)
    # prev_result = ", ".join(tile_labels)
    return image, ", ".join(tile_labels)


def get_response_fromAPI():
    response = requests.get('http://localhost:5000/output')
    if response.status_code == 200:
        data = response.json()
        print("data: ", data)
    else:
        print("failed")
    
    return str(data)

if __name__ == "__main__":
    cap=cv2.VideoCapture(1)
    cap.set(3, 640)
    cap.set(4, 480)

    # classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
    #             "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
    #             "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
    #             "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
    #             "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
    #             "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
    #             "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
    #             "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
    #             "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
    #             "teddy bear", "hair drier", "toothbrush"
    #             ]
    while True:
        real_time_predict(cap)
        # time.sleep(1)
        
    cap.release()
    cv2.destroyAllWindows()