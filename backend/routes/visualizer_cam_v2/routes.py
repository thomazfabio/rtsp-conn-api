from flask import Flask, jsonify, request, Response
import cv2
import threading
import time
from collections import deque
from . import visualizer_cam_v2

# Gerenciamento de streams ativos


class StreamManager:
    def __init__(self):
        self.streams = {}
        self.lock = threading.Lock()

    def start_stream(self, url):
        with self.lock:
            if url in self.streams:
                return False, "Stream já está ativo."
            # Criação do stream
            stream = VideoStream(url)
            if not stream.initialize():
                return False, "Erro ao inicializar o stream."
            self.streams[url] = stream
            return True, "Stream iniciado com sucesso."

    def stop_stream(self, url):
        with self.lock:
            if url not in self.streams:
                return False, "Stream não encontrado."
            self.streams[url].stop()
            del self.streams[url]
            return True, "Stream parado com sucesso."

    def get_stream(self, url):
        with self.lock:
            return self.streams.get(url)


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
        target_fps = 15  # FPS desejado
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
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                ret, buffer = cv2.imencode(
                    ".jpg",
                    frame,
                    [cv2.IMWRITE_JPEG_QUALITY, 70],
                )
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
    """
    Endpoint para iniciar um stream.
    """
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"message": "JSON inválido ou URL ausente."}), 400

    url = data["url"]
    success, message = stream_manager.start_stream(url)
    status_code = 200 if success else 500
    return jsonify({"message": message}), status_code


@visualizer_cam_v2.route("/stop_stream", methods=["POST"])
def stop_stream():
    """
    Endpoint para parar um stream.
    """
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"message": "JSON inválido ou URL ausente."}), 400

    url = data["url"]
    success, message = stream_manager.stop_stream(url)
    status_code = 200 if success else 404
    return jsonify({"message": message}), status_code


@visualizer_cam_v2.route("/stream", methods=["GET"])
def stream_video():
    """
    Endpoint para transmitir o vídeo em MJPEG com controle de taxa.
    """
    url = request.args.get("url")
    if not url:
        return jsonify({"message": "URL ausente."}), 400

    stream = stream_manager.get_stream(url)
    if not stream:
        return (
            jsonify(
                {"message": "Stream não encontrado. Use '/start_stream' primeiro."}
            ),
            404,
        )

    def generate():
            fps_limit = 15  # Limitar a 10 frames por segundo (ajustável)
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
