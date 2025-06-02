from flask import Flask, jsonify
import cv2
from real_time_prediction import real_time_predict

app = Flask(__name__)

cap=cv2.VideoCapture(1)  #預設使用Droidcam, 使用電腦配備攝像頭請將參數改為0
cap.set(3, 640)
cap.set(4, 480)
image, tile_labels = real_time_predict(cap)

@app.route('/output')
def get_output():
    image, tile_labels = real_time_predict(cap)
    return jsonify(tile_labels)

if __name__ == '__main__':
    app.run(port=5000)
