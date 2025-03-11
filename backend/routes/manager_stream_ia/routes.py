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
        if stream_id not in self.streams:
            return False, "Stream ID não encontrado."

        stream = self.streams.pop(stream_id, None)
        if stream:
            try:
                stream.stop()
                return True, f"Stream {stream_id} encerrado com sucesso."
            except Exception as e:
                print(f"Erro ao parar stream {stream_id}: {e}")
                return False, f"Erro ao parar stream: {str(e)}"
        
        return False, "Erro ao encerrar o stream."


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

        # Criamos a thread e armazenamos a referência
        self.thread = threading.Thread(target=self._start_async_loop, daemon=True)
        self.thread.start()

        return True

    def _start_async_loop(self):
        """Inicia o loop assíncrono corretamente e armazena a referência"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._read_frames())

    async def _read_frames(self):
        frame_time = 1.0 / self.fps
        try:
            while self.running:
                start_time = time.time()

                if not self.capture.isOpened():
                    print("Capture fechado, saindo do loop de leitura.")
                    break
                
                while self.running:  # <-- Adiciona condição para sair do loop se necessário
                    ret, frame = self.capture.read()
                    if not ret:
                        print("Falha ao ler frame, aguardando...")
                        await asyncio.sleep(2)
                        continue
                    if time.time() - start_time >= frame_time:
                        break  # Sai desse loop interno quando atingimos o tempo correto
                
                if not self.running:  # Verifica novamente antes de processar o frame
                    break

                frame = cv2.resize(frame, (self.width, self.height))
                ret, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                
                if ret:
                    self.buffer.append(buffer.tobytes())
                    socketio.emit(f"frame_{self.stream_id}", buffer.tobytes())

                await asyncio.sleep(max(0, frame_time - (time.time() - start_time)))

        except asyncio.CancelledError:
            print(f"Loop assíncrono da stream {self.stream_id} foi cancelado corretamente.")
        finally:
            print(f"Encerrando loop de leitura da stream {self.stream_id}.")

    



    def stop(self):
        print(f"Parando stream {self.stream_id}...")
        self.running = False  

        # Aguarda a thread encerrar antes de liberar a captura
        if hasattr(self, "thread") and self.thread.is_alive():
            print("Aguardando thread encerrar...")
            self.thread.join(timeout=2)
            if self.thread.is_alive():
                print("Thread não encerrou no tempo esperado!")

        if self.capture and self.capture.isOpened():
            self.capture.release()
            print(f"Capture liberado para {self.stream_id}")

        self.buffer.clear()

        if hasattr(self, "loop"):
            try:
                if self.loop.is_running():
                    print("Parando loop assíncrono...")

                    # Cancela todas as tarefas pendentes corretamente
                    tasks = [task for task in asyncio.all_tasks(self.loop) if not task.done()]
                    for task in tasks:
                        task.cancel()
                    print(f"Cancelando {len(tasks)} tarefas pendentes...")

                    async def shutdown():
                        await asyncio.gather(*tasks, return_exceptions=True)

                    future = asyncio.run_coroutine_threadsafe(shutdown(), self.loop)
                    future.result()  # Aguarda as tarefas cancelarem

                    self.loop.call_soon_threadsafe(self.loop.stop)

                if not self.loop.is_running() and not self.loop.is_closed():
                    print("Fechando loop assíncrono...")
                    self.loop.close()

            except RuntimeError as e:
                print(f"Erro ao encerrar loop assíncrono: {e}")

        print(f"Stream {self.stream_id} encerrado com sucesso.")



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
    print(f"Recebido pedido para parar stream {data['id']}")
    success, message = stream_manager.stop_stream(data["id"])
    emit("stop_response", {"success": success, "message": message})
    print(f"Resposta enviada: {message}")


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
