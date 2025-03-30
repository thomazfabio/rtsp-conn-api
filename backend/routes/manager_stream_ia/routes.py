from flask import Blueprint, request
from flask_socketio import SocketIO, emit
import cv2
import asyncio
import time
import threading
from collections import deque

# Criando a Blueprint para streaming
streaming_ia_bp = Blueprint("streaming", __name__)
socketio = SocketIO()

class StreamManager:
    def __init__(self):
        self.streams = {}
        self.lock = threading.Lock()

    def start_stream(self, stream_id, url, width, height, fps, permanente):
        with self.lock:
            if stream_id in self.streams:
                return False, "Stream já está ativo."
            stream = VideoStream(stream_id, url, width, height, fps, permanente)
            if not stream.initialize():
                return False, "Erro ao inicializar o stream."
            self.streams[stream_id] = stream
            return True, "Stream iniciado com sucesso."

    def stop_stream(self, stream_id):
        with self.lock:
            stream = self.streams.pop(stream_id, None)
            if stream:
                stream.stop()
                return True, f"Stream {stream_id} encerrado com sucesso."
            return False, "Stream ID não encontrado."

    def get_stream(self, stream_id):
        with self.lock:
            return self.streams.get(stream_id)

class VideoStream:
    def __init__(self, stream_id, url, width, height, fps, permanente):
        self.stream_id = stream_id
        self.url = url
        self.width = width
        self.height = height
        self.fps = fps
        self.permanente = permanente
        self.capture = None
        self.running = False
        self.buffer = deque(maxlen=60)
        self.last_viewer_time = time.time()
        self.loop = asyncio.get_event_loop()
        self.thread = None

    def initialize(self):
        """Inicializa a captura e inicia a thread para leitura assíncrona."""
        self.capture = cv2.VideoCapture(self.url)
        if not self.capture.isOpened():
            return False
        self.running = True
        self.thread = threading.Thread(target=self._start_reading, daemon=True)
        self.thread.start()
        return True

    def _start_reading(self):
        """Executa a leitura de frames em uma thread separada sem bloquear."""
        asyncio.run_coroutine_threadsafe(self._read_frames(), self.loop)

    async def _read_frames(self):
        frame_time = 1.0 / self.fps
        try:
            while self.running:
                start_time = time.time()
                if not self.capture.isOpened():
                    print("Capture fechado, saindo do loop de leitura.")
                    break
                
                ret, frame = self.capture.read()
                if not ret:
                    print("Falha ao ler frame, aguardando...")
                    await asyncio.sleep(2)
                    continue
                
                frame = cv2.resize(frame, (self.width, self.height))
                ret, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                if ret:
                    self.buffer.append(buffer.tobytes())
                    socketio.emit(f"frame_{self.stream_id}", buffer.tobytes())
                
                await asyncio.sleep(max(0, frame_time - (time.time() - start_time)))
        except asyncio.CancelledError:
            print(f"Loop assíncrono da stream {self.stream_id} cancelado corretamente.")
        finally:
            print(f"Encerrando loop de leitura da stream {self.stream_id}.")

    def stop(self):
        print(f"Parando stream {self.stream_id}...")
        self.running = False
        if self.capture and self.capture.isOpened():
            self.capture.release()
            print(f"Capture liberado para {self.stream_id}")
        self.buffer.clear()

        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)

        print("Stream encerrada.")

stream_manager = StreamManager()

@socketio.on("start_stream")
def handle_start_stream(data):
    success, message = stream_manager.start_stream(
        data["id"], data["url"], data["width"], data["height"], data["fps"], data["permanente"]
    )
    emit("start_response", {"success": success, "message": message})

@socketio.on("stop_stream")
def handle_stop_stream(data):
    success, message = stream_manager.stop_stream(data["id"])
    emit("stop_response", {"success": success, "message": message})

@socketio.on("subscribe_stream")
def handle_subscribe_stream(data):
    stream = stream_manager.get_stream(data["id"])
    if stream:
        stream.last_viewer_time = time.time()
    else:
        emit("error", {"message": "Stream não encontrado."})

@socketio.on("teste")
def test_connect():
    print("Client connected")
    emit("teste", {"message": "Teste de conexão com sucesso."})

@socketio.on("conectar")
def handle_connect():
    print("Cliente conectado!")
    socketio.emit("conectado", {"msg": "Bem-vindo ao servidor WebSocket!"})

@streaming_ia_bp.route("/teste")
def teste():
    return "Teste"
