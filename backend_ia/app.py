import asyncio
import websockets
import cv2
import numpy as np
import torch

def process_frame_on_gpu(frame):
    # Certifica-se de que o frame está no formato esperado (RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Converte o frame para tensor, normaliza para 0-1 e move para a GPU
    frame_tensor = torch.from_numpy(frame_rgb).float().to("cuda") / 255.0

    # Se necessário, realiza a conversão para grayscale
    gray_frame = 0.2989 * frame_tensor[:, :, 0] + 0.5870 * frame_tensor[:, :, 1] + 0.1140 * frame_tensor[:, :, 2]

    # Converte de volta para uma imagem de 8 bits e move de volta para a CPU
    processed_frame = (gray_frame * 255).byte().cpu().numpy()

    # Converte de volta para o formato BGR para exibição
    processed_frame_bgr = cv2.cvtColor(processed_frame, cv2.COLOR_GRAY2BGR)

    return processed_frame_bgr

# Função para exibir a janela do OpenCV
def display_frame(frame):
    cv2.imshow("Processed Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Fecha a janela com a tecla 'q'
        cv2.destroyAllWindows()

# Função WebSocket que recebe os frames e executa a inferência
async def handle_frame(websocket):
    try:
        async for message in websocket:
            # Exibe os detalhes da mensagem recebida
            print(f"[INFO] Tipo da mensagem recebida: {type(message)}")
            print(f"[INFO] Tamanho da mensagem recebida (em bytes): {len(message)}")

            # Converte a mensagem em um array de bytes
            frame_bytes = np.frombuffer(message, np.uint8)

            print(f"[INFO] Tipo do frame após decodificação: {type(frame_bytes)}")
            # Decodifica o frame para o formato da imagem
            frame = cv2.imdecode(frame_bytes, cv2.IMREAD_COLOR)
            print(f"[INFO] Dimensões do frame: {frame.shape}")

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
