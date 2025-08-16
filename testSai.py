from flask import Flask, Response
from picamera2 import Picamera2
import cv2

app = Flask(__name__)

tuning_data = Picamera2.load_tuning_file("/home/mrm/xxx.json")
# Initialize camera without custom tuning file
picam2 = Picamera2(tuning=tuning_data)
# Comment out custom tuning file to test default

config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (1000, 1000)})
picam2.configure(config)
picam2.start()
print("Camera started with default tuning!")

def generate_frames():
    while True:
        frame = picam2.capture_array()
#        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
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
