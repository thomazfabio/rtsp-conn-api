import asyncio
import cv2
import numpy as np
import torch
from asyncio import Queue

frame_queue = Queue(maxsize=10)  # Limita a fila para evitar sobrecarga da CPU
camera_url = "rtsp://admin:227802@192.168.15.150:554/cam/realmonitor?channel=1&subtype=0"  # Altere para sua câmera

# Função para converter a imagem para escala de cinza na GPU
def process_frame_on_gpu(frame):
    # Converte o frame para tensor e move para a GPU
    frame_tensor = torch.from_numpy(frame).float().to("cuda") / 255.0

    # Converte para escala de cinza (usando as fórmulas de RGB para Y)
    gray_frame = frame_tensor[:, :, 0] * 0.2989 + frame_tensor[:, :, 1] * 0.5870 + frame_tensor[:, :, 2] * 0.1140

    # Converte de volta para formato uint8 e expande para 3 canais para OpenCV
    processed_frame = (gray_frame * 255).byte()
    processed_frame = processed_frame.unsqueeze(2).expand(-1, -1, 3)  # Expande para 3 canais (RGB)
    
    return processed_frame.cpu().numpy()

# Consumidor de frames usando GPU
async def process_frame():
    while True:
        frame_bytes = await frame_queue.get()  # Aguarda um frame na fila
        nparr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # OpenCV usa CPU aqui

        # Ajuste para a resolução fixa 640x480
        frame = cv2.resize(frame, (640, 480))

        # Envia para GPU e processa
        processed_frame = process_frame_on_gpu(frame)

        # Exibe a imagem processada em uma janela
        cv2.imshow("Processed Video", processed_frame)

        # Verifica se a janela foi fechada ou se a tecla 'q' foi pressionada
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_queue.task_done()  # Marca como concluído

# Produtor de frames (captura da câmera)
async def capture_frames():
    cap = cv2.VideoCapture(camera_url)

    if not cap.isOpened():
        print("Erro ao abrir a câmera!")
        return

    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Evita armazenar muitos frames na memória

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar frame.")
            await asyncio.sleep(0.1)
            continue

        # Redimensiona para 640x480
        frame = cv2.resize(frame, (640, 480))

        # Codifica o frame como JPEG
        _, buffer = cv2.imencode(".jpg", frame)
        await frame_queue.put(buffer.tobytes())  # Adiciona frame na fila

        await asyncio.sleep(0.03)  # Ajuste para não sobrecarregar a CPU

# Gerenciador principal
async def main():
    num_consumers = 3  # Número de processadores paralelos
    consumers = [asyncio.create_task(process_frame()) for _ in range(num_consumers)]
    producer = asyncio.create_task(capture_frames())  # Captura os frames

    await asyncio.gather(producer, *consumers)  # Executa tudo em paralelo

# Inicia o loop assíncrono
asyncio.run(main())

# Libera a janela após a execução
cv2.destroyAllWindows()
