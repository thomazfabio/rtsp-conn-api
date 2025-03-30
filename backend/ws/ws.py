import asyncio
import websockets
import base64

SERVER_URL = "ws://192.168.15.155:8000/ws/1"

async def send_frame_to_server(frame):
    """Abre a conexão WebSocket e envia o frame."""
    try:
        async with websockets.connect(SERVER_URL) as websocket:
            frame64 = base64.b64encode(frame).decode('utf-8')
            await websocket.send(frame64)
            print("[INFO] Frame enviado!")
    except Exception as e:
        print(f"[ERROR] Erro ao enviar frame: {e}")

def send_frame(frame):
    """Executa a função assíncrona sem precisar de loop global."""
    asyncio.run(send_frame_to_server(frame))
