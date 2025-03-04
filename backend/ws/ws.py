import asyncio
import websockets
import numpy as np

# Variáveis de configuração
SERVER_URL = "ws://localhost:8765"  # URL do servidor de inferência WebSocket (ajuste conforme necessário)

# Função para iniciar a conexão WebSocket
async def connect_to_inference_server():
    async with websockets.connect(SERVER_URL) as websocket:
        print(f"[INFO] Conectado ao servidor WebSocket em {SERVER_URL}")
        return websocket

# Função para enviar o frame para o servidor de inferência
async def send_frame_to_inference_server(frame):
    try:
        # Conecta ao servidor
        async with websockets.connect(SERVER_URL) as websocket:
            print(f"[INFO] Enviando frame para o servidor de inferência...")
            
            # Codifica o frame para enviar como bytes (se necessário)
            message = frame.tobytes()

            # Envia o frame como bytes para o servidor
            await websocket.send(message)
            print("[INFO] Frame enviado!")

    except Exception as e:
        print(f"[ERROR] Erro ao conectar/enviar para o servidor: {e}")

# Função para ser chamada em outro arquivo que passará o frame
def send_frame(frame):
    asyncio.run(send_frame_to_inference_server(frame))
