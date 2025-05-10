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

## Run the model
下載這個檔案並解壓縮 (建議使用WinRAR)
[text](https://drive.google.com/file/d/1zmgVjSa2nh4hwUGe5Pv9Msf3DVUH5B7M/view?usp=drive_link)

將```train2017```裡的圖片 (xxxxxx.jpg) 全部貼到```dataset/images/train```資料夾下面 (不要再包多的資料夾)
將```val2017```裡的圖片 (xxxxxx.jpg) 全部貼到```dataset/images/val```資料夾下面 (不要再包多的資料夾)

執行 ```test..py```






