from flask import Flask, jsonify, request, Response
import cv2
import threading
import asyncio
import time
import base64
import uuid
from collections import deque
from . import visualizer_cam_v2
from ws.ws import send_frame
# Gerenciamento de streams ativos

class StreamManager:
    def __init__(self):
        self.streams = {}
        self.lock = threading.Lock()

    def start_stream(self, url):
        with self.lock:
            # Criar um ID único para o stream
            stream_id = str(uuid.uuid4())

            # Criar e iniciar o stream
            stream = VideoStream(url)
            if not stream.initialize():
                return False, "Erro ao inicializar o stream."

            # Armazenar o stream no dicionário usando o ID
            self.streams[stream_id] = stream

            return True, stream_id  # Retorna o ID gerado

    def stop_stream(self, stream_id):
        with self.lock:
            if stream_id not in self.streams:
                return False, "Stream não encontrado."

            self.streams[stream_id].stop()
            del self.streams[stream_id]
            return True, "Stream parado com sucesso."

    def get_stream(self, stream_id):
        with self.lock:
            return self.streams.get(stream_id)

# Gerenciamento individual de stream
class VideoStream:
    def __init__(self, url):
        self.url = url
        self.capture = None
        self.thread = None
        self.running = False
        # Buffer de 2 segundos para estabilizar (30 FPS)
        self.buffer = deque(maxlen=60)
        self.lock = threading.Lock()

    def initialize(self):
        self.capture = cv2.VideoCapture(self.url)
        if not self.capture.isOpened():
            return False
        self.running = True
        self.thread = threading.Thread(target=self._read_frames, daemon=True)
        self.thread.start()
        return True


    def _read_frames(self):
        target_fps = 16  # FPS desejado
        frame_time = 1.0 / target_fps  # Tempo ideal entre frames

        while self.running:
            start_time = time.time()

            with self.lock:
                if not self.running:
                    break

                # Descarta frames antigos e pega o mais recente
                while True:
                    ret, frame = self.capture.read()
                    if not ret:
                        print(
                            f"Erro: Não foi possível ler o frame do stream {self.url}."
                        )
                        time.sleep(2)
                        break

                    # Aguarda um pequeno tempo para garantir que pegamos o frame mais recente
                    if time.time() - start_time >= frame_time:
                        break

            if ret:
                frame = cv2.resize(frame, (640, 480))
                #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Tipo do frame (normalmente será numpy.ndarray se for uma imagem do OpenCV)          
                # Codifica o frame em JPEG         
                ret, buffer = cv2.imencode(
                    ".jpg",
                    frame,
                    [cv2.IMWRITE_JPEG_QUALITY,70],
                )  
                #converte para base 64 json                 
                if ret:
                    self.buffer.append(buffer.tobytes())
                    
            # Garante que respeitamos o FPS
            elapsed_time = time.time() - start_time
            sleep_time = max(0, frame_time - elapsed_time)
            time.sleep(sleep_time)

    def get_frame(self):
        with self.lock:
            if self.buffer:
                # Retorna o frame mais recente no buffer
                return self.buffer[-1]
            return None

    def stop(self):
        with self.lock:
            self.running = False
        if self.thread:
            self.thread.join()
        if self.capture and self.capture.isOpened():
            self.capture.release()
        # Limpa o buffer para remover frames antigos
        with self.lock:
            self.buffer.clear()


# Instância global do gerenciador de streams
stream_manager = StreamManager()


@visualizer_cam_v2.route("/start_stream", methods=["POST"])
def start_stream():
    data = request.get_json()
    if not data or "url_rtsp" not in data:
        return jsonify({"message": "JSON inválido ou URL ausente."}), 400

    url = data["url_rtsp"]
    success, stream_id = stream_manager.start_stream(url)

    if success:
        return jsonify({
            "message": "Stream iniciado com sucesso",
            "stream_id": stream_id,
            "stream_url": f"http://127.0.0.1:5000/visualizer_cam_v2/stream?stream_id={stream_id}"
        }), 200
    else:
        return jsonify({"message": stream_id}), 500



@visualizer_cam_v2.route("/stop_stream", methods=["POST"])
def stop_stream():
    data = request.get_json()
    if not data or "stream_id" not in data:
        return jsonify({"message": "JSON inválido ou stream_id ausente."}), 400

    stream_id = data["stream_id"]
    success, message = stream_manager.stop_stream(stream_id)
    return jsonify({"message": message}), 200 if success else 404



@visualizer_cam_v2.route("/stream", methods=["GET"])
def stream_video():
    stream_id = request.args.get("stream_id")
    if not stream_id:
        return jsonify({"message": "stream_id ausente."}), 400

    stream = stream_manager.get_stream(stream_id)
    if not stream:
        return jsonify({"message": "Stream não encontrado."}), 404

    def generate():
        fps_limit = 16  # Limitar a 10 frames por segundo (ajustável)
        frame_interval = 1 / fps_limit
        last_frame_time = time.time()

        while True:
            frame = stream.get_frame()
            if frame:
                current_time = time.time()
                if current_time - last_frame_time >= frame_interval:
                    last_frame_time = current_time
                    yield (
                        b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                    )
            else:
                time.sleep(0.1)  # Aguarda até que um frame esteja disponível

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")
