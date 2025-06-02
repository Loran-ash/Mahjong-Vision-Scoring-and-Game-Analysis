# [Mahjong-Vision-Scoring-and-Game-Analysis](https://github.com/Loran-ash/Mahjong-Vision-Scoring-and-Game-Analysis)

#### We aim to recognize Mahjong tiles through photo capture and real-time image recognition. Based on the identified tiles, the system can then provide tile discard suggestions.

![Last Commit](https://img.shields.io/github/last-commit/Loran-ash/Mahjong-Vision-Scoring-and-Game-Analysis)
![Language](https://img.shields.io/github/languages/top/Loran-ash/Mahjong-Vision-Scoring-and-Game-Analysis)
![GitHub stars](https://img.shields.io/github/stars/Loran-ash/Mahjong-Vision-Scoring-and-Game-Analysis)



## Setup instruction
Install the ultralytics package from PyPI (Pytorch shuld be prepared.)
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

Download this folder and unzip it. (WinRAR is recommanded)
[Link](https://drive.google.com/file/d/1zmgVjSa2nh4hwUGe5Pv9Msf3DVUH5B7M/view?usp=drive_link)

Paste all the images (xxxxxx.jpg) from ``train2017`` into the ``dataset/images/train`` folder (don't wrap any more folders).

Paste all the images (xxxxxx.jpg) from ``val2017`` into the ``dataset/images/val`` folder (don't wrap any more folders).

Run ```test_train.py```

>You can also refer to our dataset: [Link](https://drive.google.com/drive/folders/1tJOyyNNLBpiCzEqrtbJePKiDOmigqr1a?usp=sharing)


## Make a prediction with trained models

Put the image you want to predict into the ```test_images`` folder.

```python
from test_pred import prediction
result = prediction() # 也可以填入模型路徑 (string) 作為引數
```

Or just run ```test_pred.py```

## Example results

![Image](https://github.com/user-attachments/assets/81807b03-ea41-4759-ba3f-f03b5722454d)

## Launch 🀄️ 麻將向聽計算器 Mahjong Waits Calculator

Run the coomands
```bash
python page.py
```
This will launch WebUI，the port is on ```http://localhost:7860/``` by default.


```bash
python real_time_API.py
```
For some technical reasons, this will provide the function to capture webcam images.

>Note: We set the webcam as ```cap=cv2.VideoCapture(1)``` by default. In case you have other cameras, just change the parameter (ex: ```cap=cv2.VideoCapture(0)```).

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






