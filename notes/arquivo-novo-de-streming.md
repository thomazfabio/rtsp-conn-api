Para adicionar essa funcionalidade sem alterar muito o seu código, podemos seguir essa abordagem:  

1. **Adicionar um modo para cada stream** → O `StreamManager` precisa saber se o stream está **apenas para visualização** ou se está **sendo processado por IA**. Podemos adicionar um campo `mode` com valores `"streaming"` ou `"processing"`.  
2. **Monitoramento de espectadores** → Cada stream precisa saber se está sendo **acessado por alguém** pelo endpoint `/stream`. Se ninguém acessar por 10 segundos, o stream deve ser encerrado **apenas se for do tipo "streaming"**.  
3. **Criar um contador de acessos** → Podemos armazenar a última vez que o stream foi acessado e encerrar automaticamente se ninguém estiver assistindo.  

---

### **Implementação das mudanças**
Vou modificar sua classe `StreamManager` e `VideoStream` para incluir esse controle:  

```python
import time
import threading
import cv2
from collections import deque
from flask import Flask, jsonify, request, Response
from . import visualizer_cam_v2

# Gerenciamento de streams ativos
class StreamManager:
    def __init__(self):
        self.streams = {}
        self.lock = threading.Lock()

    def start_stream(self, url, mode="streaming"):
        with self.lock:
            if url in self.streams:
                return False, "Stream já está ativo."
            stream = VideoStream(url, mode)
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
    def __init__(self, url, mode="streaming"):
        self.url = url
        self.mode = mode  # "streaming" ou "processing"
        self.capture = None
        self.thread = None
        self.running = False
        self.buffer = deque(maxlen=60)  # Buffer de 2 segundos para estabilizar (30 FPS)
        self.lock = threading.Lock()
        self.last_access_time = time.time()  # Tempo do último acesso ao stream

    def initialize(self):
        self.capture = cv2.VideoCapture(self.url)
        if not self.capture.isOpened():
            return False
        self.running = True
        self.thread = threading.Thread(target=self._read_frames, daemon=True)
        self.thread.start()
        # Criar thread para monitorar tempo de acesso (somente para streaming)
        if self.mode == "streaming":
            threading.Thread(target=self._monitor_access, daemon=True).start()
        return True

    def _read_frames(self):
        while self.running:
            with self.lock:
                if not self.running:
                    break
                ret, frame = self.capture.read()
                if not ret:
                    print(f"Erro: Não foi possível ler o frame do stream {self.url}.")
                    time.sleep(2)
                    continue

                frame = cv2.resize(frame, (640, 480))
                ret, buffer = cv2.imencode('.jpg', frame)
                if ret:
                    self.buffer.append(buffer.tobytes())

            time.sleep(0.00)  # Ajuste para consumo de CPU

    def _monitor_access(self):
        """Monitora se o stream está sendo assistido e fecha após 10s sem acesso (apenas streaming)."""
        while self.running and self.mode == "streaming":
            time.sleep(10)
            with self.lock:
                if time.time() - self.last_access_time > 10:
                    print(f"Stream {self.url} fechado por inatividade.")
                    self.stop()
                    return

    def get_frame(self):
        with self.lock:
            self.last_access_time = time.time()  # Atualiza o tempo do último acesso
            return self.buffer[-1] if self.buffer else None

    def stop(self):
        with self.lock:
            self.running = False
        if self.thread:
            self.thread.join()
        if self.capture and self.capture.isOpened():
            self.capture.release()


# Instância global do gerenciador de streams
stream_manager = StreamManager()

@visualizer_cam_v2.route('/start_stream', methods=['POST'])
def start_stream():
    """
    Endpoint para iniciar um stream.
    """
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"message": "JSON inválido ou URL ausente."}), 400

    url = data['url']
    mode = data.get('mode', 'streaming')  # Se não for informado, assume "streaming"
    
    success, message = stream_manager.start_stream(url, mode)
    status_code = 200 if success else 500
    return jsonify({"message": message}), status_code

@visualizer_cam_v2.route('/stop_stream', methods=['POST'])
def stop_stream():
    """
    Endpoint para parar um stream.
    """
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"message": "JSON inválido ou URL ausente."}), 400

    url = data['url']
    success, message = stream_manager.stop_stream(url)
    status_code = 200 if success else 404
    return jsonify({"message": message}), status_code

@visualizer_cam_v2.route('/stream', methods=['GET'])
def stream_video():
    """
    Endpoint para transmitir o vídeo em MJPEG com controle de taxa.
    """
    url = request.args.get('url')
    if not url:
        return jsonify({"message": "URL ausente."}), 400

    stream = stream_manager.get_stream(url)
    if not stream:
        return jsonify({"message": "Stream não encontrado. Use '/start_stream' primeiro."}), 404

    def generate():
        fps_limit = 15
        frame_interval = 1 / fps_limit
        last_frame_time = time.time()

        while True:
            frame = stream.get_frame()
            if frame:
                current_time = time.time()
                if current_time - last_frame_time >= frame_interval:
                    last_frame_time = current_time
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                time.sleep(0.1)

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
```

---

### **O que mudou?**
✅ **Adicionamos um modo para cada stream** (`mode="streaming"` ou `mode="processing"`).  
✅ **Criamos um sistema para monitorar o último acesso** ao stream.  
✅ **Se um stream for do tipo "streaming" e ficar 10 segundos sem acesso, ele é encerrado automaticamente**.  
✅ **Streams do tipo "processing" nunca são encerrados automaticamente**.  

### **Como usar?**
1️⃣ **Iniciar um stream normal (apenas visualização)**:  
```json
{
    "url": "rtsp://minhacamera",
    "mode": "streaming"
}
```
📌 **Se ninguém acessar `/stream?url=rtsp://minhacamera` por 10s, ele será fechado.**  

2️⃣ **Iniciar um stream para processamento (IA rodando em paralelo)**:  
```json
{
    "url": "rtsp://minhacamera",
    "mode": "processing"
}
```
📌 **Esse stream **NÃO** será fechado automaticamente, mesmo sem acessos.**  

---

### **Conclusão**
Essa solução mantém a compatibilidade com seu código atual, adicionando a funcionalidade de **fechar streams sem uso** sem impactar os que estão processando IA. 🚀