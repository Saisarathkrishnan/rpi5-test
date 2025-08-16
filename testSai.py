# camera_stream.py
import json
from picamera2 import Picamera2
from flask import Flask, Response
import cv2
import os
import time

app=Flask(__name__)
# Load JSON tuning file
with open("/home/mrm/xxx.json") as f:
    controls_json = json.load(f)


picam2 = Picamera2()
if "controls" in controls_json:
    for key, value in controls_json["controls"].items():
        picam2.set_controls({key: value})
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
picam2.configure(config)
picam2.start()

print("Camera started with tuning!")

time.sleep(5)
def generate_frames():
    while True:
        frame = picam2.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return '<h1>RPi Camera Stream</h1><img src="/video_feed">'

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
