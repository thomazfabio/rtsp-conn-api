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
            if stream_id not in self.streams:
                return False, "Stream não encontrado."
            self.streams[stream_id].stop()
            del self.streams[stream_id]
            return True, "Stream parado com sucesso."

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

    def initialize(self):
        self.capture = cv2.VideoCapture(self.url)
        if not self.capture.isOpened():
            return False
        self.running = True

        # Iniciar thread para rodar a função assíncrona
        threading.Thread(target=self._start_async_loop, daemon=True).start()
        return True

    def _start_async_loop(self):
        """Inicia o loop assíncrono corretamente e armazena a referência"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._read_frames())

    async def _read_frames(self):
        frame_time = 1.0 / self.fps
        while self.running:
            start_time = time.time()
           
            while True:
                ret, frame = self.capture.read()
                if not ret:
                    await asyncio.sleep(2)
                    continue
                # Aguarda um pequeno tempo para garantir que pegamos o frame mais recente
                if time.time() - start_time >= frame_time:
                 break
             
            frame = cv2.resize(frame, (self.width, self.height))
            ret, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
            if ret:
                self.buffer.append(buffer.tobytes())
                socketio.emit(f"frame_{self.stream_id}", buffer.tobytes())
                print(f"Enviando frame para frame_{self.stream_id}")
            await asyncio.sleep(max(0, frame_time - (time.time() - start_time)))

  
def stop(self):
    self.running = False
    if self.capture and self.capture.isOpened():
        self.capture.release()
    self.buffer.clear()

    # Se o loop assíncrono estiver rodando, pare-o corretamente
    if hasattr(self, "loop"):
        try:
            if self.loop.is_running():
                self.loop.call_soon_threadsafe(self.loop.stop)

                # Pequeno atraso para garantir que o loop pare
                time.sleep(0.2)

            # Agora, fechamos o loop sem interromper o servidor
            if not self.loop.is_closed():
                self.loop.call_soon_threadsafe(self.loop.close)
                
        except RuntimeError as e:
            print(f"Erro ao encerrar loop assíncrono: {e}")


stream_manager = StreamManager()


@socketio.on("start_stream")
def handle_start_stream(data):
    success, message = stream_manager.start_stream(
        data["id"],
        data["url"],
        data["width"],
        data["height"],
        data["fps"],
        data["permanente"],
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
def handle_connect(data=None):
    print("Cliente conectado!")
    socketio.emit("conectado", {"msg": "Bem-vindo ao servidor WebSocket!"})


@streaming_ia_bp.route("/teste")
def teste():
    return "Teste"
