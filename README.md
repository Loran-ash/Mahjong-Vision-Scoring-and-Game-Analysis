# [Mahjong-Vision-Scoring-and-Game-Analysis](https://github.com/Loran-ash/Mahjong-Vision-Scoring-and-Game-Analysis)

#### We aim to recognize Mahjong tiles through photo capture and real-time image recognition. Based on the identified tiles, the system can then provide tile discard suggestions.

![Last Commit](https://img.shields.io/github/last-commit/Loran-ash/Mahjong-Vision-Scoring-and-Game-Analysis)
![Language](https://img.shields.io/github/languages/top/Loran-ash/Mahjong-Vision-Scoring-and-Game-Analysis)
![GitHub stars](https://img.shields.io/github/stars/Loran-ash/Mahjong-Vision-Scoring-and-Game-Analysis)



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
We are training the model with [YOLOv11](https://docs.ultralytics.com/)

下載這個檔案並解壓縮 (建議使用WinRAR)
[Link](https://drive.google.com/file/d/1zmgVjSa2nh4hwUGe5Pv9Msf3DVUH5B7M/view?usp=drive_link)

將```train2017```裡的圖片 (xxxxxx.jpg) 全部貼到```dataset/images/train```資料夾下面 (不要再包多的資料夾)

將```val2017```裡的圖片 (xxxxxx.jpg) 全部貼到```dataset/images/val```資料夾下面 (不要再包多的資料夾)

執行 ```test_train.py```

>也可參考我們自製的資料集 [Link](https://drive.google.com/drive/folders/1tJOyyNNLBpiCzEqrtbJePKiDOmigqr1a?usp=sharing)


## Make a prediction with trained models

將想辨識的圖片放進```test_images```資料夾裡面。

```python
from test_pred import prediction
result = prediction() # 也可以填入模型路徑 (string) 作為引數
```

或直接執行```test_pred.py```

result可被視覺化，請將```test_pred.py```，if __name__ == "__main__": 的註解部份去掉，再直接執行。

## Example results

![Image](https://github.com/user-attachments/assets/81807b03-ea41-4759-ba3f-f03b5722454d)

## Launch 🀄️ 麻將向聽計算器 Mahjong Waits Calculator

Run the coomands
```bash
python page.py
```
這將會啟動WebUI，預設在```http://localhost:7860/```

```bash
python real_time_API.py
```
因為某些技術上的原因，這將提供擷取網路攝像頭影像的功能。

### Usage Demonstration

![Image](https://github.com/user-attachments/assets/8c540ffa-77ad-46b2-9990-546ccc54c076)
![Image](https://github.com/user-attachments/assets/61b1e934-8202-4d2f-9c69-8a1cd65cd070)

## Contributors

Thanks to everyone contributing to this project, including those not mentioned here.

<ul>
  <li>
    <img src='https://avatars.githubusercontent.com/u/131962510?v=4' height='28' width='28'></img>&nbsp;&nbsp;<strong><a href='https://github.com/Loran-ash'>Loran-ash</a></strong>
    <ul>
      <li>Loran is in charge of real-time image recognition and model training, optimizing system performance.</li>
    </ul>
  </li>
  <li>
    <img src='https://avatars.githubusercontent.com/u/150805993?v=4' height='28' width='28'></img>&nbsp;&nbsp;<strong><a href='https://github.com/yukki0728'>yukki0728</a></strong>
    <ul>
      <li>Yukki is responsible for capturing and annotating the dataset.</li>
    </ul>
  </li>
  <li>
    <img src='https://avatars.githubusercontent.com/u/190680637?v=4' height='28' width='28'></img>&nbsp;&nbsp;<strong><a href='https://github.com/Elainechen14'>Elainechen14</a></strong>
    <ul>
      <li>Elaine handles the web UI development and contributes to model training for user interaction.</li>
    </ul>
  </li>
</ul>

## Reference

1. https://huggingface.co/spaces/awacke1/WebRTC-Yolov10-Webcam-Stream-1/tree/9ffc08341a687f4134da043f2265d4c009bbd22c
2. https://github.com/jaheel/MJOD-2136
3. https://www.gradio.app/
4. https://docs.ultralytics.com/
5. https://blog.csdn.net/weixin_44133371/article/details/137357947
6. https://blog.csdn.net/qiaoyurensheng/article/details/123410218






