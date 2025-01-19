from flask import Flask, Response
import cv2

app = Flask(__name__)

def generate_frames(rtsp_url):
    # Abre o stream RTSP com OpenCV
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        raise RuntimeError("Não foi possível abrir o stream RTSP.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Codifica o frame como JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Transmite o frame como parte do fluxo MJPEG
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@app.route('/stream')
def stream():
    # Insira a URL RTSP do vídeo
    rtsp_url = "rtsp://sua_camera_url_aqui"
    return Response(generate_frames(rtsp_url),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


