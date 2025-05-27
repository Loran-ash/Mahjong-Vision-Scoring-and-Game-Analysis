## Setup instruction
Install the ultralytics package from PyPI (要先準備好Pytorch)
```sh
pip install -U ultralytics
```

## Note
這個dataset原本是COCO style format (json)，不能直接丟進YOLO，須使用轉換器轉成每張圖片對應一個.txt label
它應該要長成這樣：
```
dataset/
├── images/
│   ├── train/
│   └── val/
├── labels/
│   ├── train/
│   └── val/
└── data.yaml
```
在```json2yolo.py```已經處理了這件事，只是記錄一下，各位可以不用管這一塊。


## Train the model
下載這個檔案並解壓縮 (建議使用WinRAR)
[Link](https://drive.google.com/file/d/1zmgVjSa2nh4hwUGe5Pv9Msf3DVUH5B7M/view?usp=drive_link)

將```train2017```裡的圖片 (xxxxxx.jpg) 全部貼到```dataset/images/train```資料夾下面 (不要再包多的資料夾)

將```val2017```裡的圖片 (xxxxxx.jpg) 全部貼到```dataset/images/val```資料夾下面 (不要再包多的資料夾)

執行 ```test_train.py```


## Make a prediction with trained models

將想辨識的圖片放進```test_images```資料夾裡面。

```python
from test_pred import prediction
result = prediction() # 也可以填入模型路徑 (string) 作為引數
```

或直接執行```test_pred.py```

result可被視覺化，請將```test_pred.py```，if __name__ == "__main__": 的註解部份去掉，再直接執行。

## Reference

1. https://huggingface.co/spaces/awacke1/WebRTC-Yolov10-Webcam-Stream-1/tree/9ffc08341a687f4134da043f2265d4c009bbd22c






