import asyncio
import websockets
import cv2
import numpy as np
import torch

# Função de inferência na GPU (simulada)
def process_frame_on_gpu(frame):
    frame_tensor = torch.from_numpy(frame).float().to("cuda") / 255.0
    gray_frame = 0.2989 * frame_tensor[:, :, 0] + 0.5870 * frame_tensor[:, :, 1] + 0.1140 * frame_tensor[:, :, 2]
    processed_frame = (gray_frame * 255).byte().cpu().numpy()
    return processed_frame

# Função para exibir a janela do OpenCV
def display_frame(frame):
    cv2.imshow("Processed Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Fecha a janela com a tecla 'q'
        cv2.destroyAllWindows()

# Função WebSocket que recebe os frames e executa a inferência
async def handle_frame(websocket, path):
    try:
        async for message in websocket:
            # A mensagem recebida é um frame em bytes
            nparr = np.frombuffer(message, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Processa o frame na GPU
            processed_frame = process_frame_on_gpu(frame)

            # Exibe a janela com o frame processado
            display_frame(processed_frame)
            
            print("[INFO] Frame processado!")

    except Exception as e:
        print(f"[ERROR] Erro ao processar o frame: {e}")

# Função para iniciar o servidor WebSocket
async def start_server():
    # Defina a porta que o servidor irá usar
    server_port = 8765  # Porta padrão, altere conforme necessário
    print(f"[INFO] Servidor WebSocket iniciado na porta {server_port}")
    
    async with websockets.serve(handle_frame, "localhost", server_port):
        await asyncio.Future()  # Mantém o servidor rodando indefinidamente

# Inicia o servidor
if __name__ == "__main__":
    asyncio.run(start_server())
