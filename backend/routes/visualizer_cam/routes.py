from flask import jsonify, request, Response
from . import visualizer_cam  # Importando o Blueprint definido no __init__.py
import cv2

# Variáveis globais
video_capture = None
current_url = None  # Armazena a URL atual para evitar reaberturas desnecessárias

def open_video(url):
    """
    Abre o stream RTSP usando OpenCV.
    """
    global video_capture, current_url

    # Fecha qualquer conexão aberta anteriormente
    if video_capture:
        video_capture.release()
        video_capture = None

    # Abre o novo stream RTSP
    video_capture = cv2.VideoCapture(url)

    if not video_capture.isOpened():
        print("Erro: Não foi possível abrir o stream RTSP.")
        video_capture = None  # Reseta a variável para evitar uso de uma conexão inválida
        return False
    else:
        print("Conexão com o stream RTSP bem-sucedida.")
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        print(f"Taxa de quadros (FPS): {fps}")
        current_url = url  # Atualiza a URL ativa
        return True

def generate_frames():
    """
    Gera frames do stream RTSP em formato JPEG.
    """
    global video_capture
    while (True):
        if video_capture is None or not video_capture.isOpened():
            print("Erro: Stream não está aberto.")
            break

        ret, frame = video_capture.read()
        if not ret:
            print("Erro: Não foi possível ler o frame do stream.")
            break

        # Codifica o frame em JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("Erro: Não foi possível codificar o frame.")
            break

        # Converte o buffer para bytes
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@visualizer_cam.route('/simple', methods=['POST'])
def simple():
    """
    Endpoint para inicializar o stream RTSP.
    """
    global video_capture, current_url
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"message": "JSON inválido ou URL ausente."}), 400

    url = data['url']

    # Verifica se o stream já está ativo com a mesma URL
    if video_capture and video_capture.isOpened() and current_url == url:
        return jsonify({"message": "Stream já está ativo com a URL fornecida."}), 200

    # Tenta abrir o novo stream
    if open_video(url):
        return jsonify({"message": "Conexão com o stream RTSP bem-sucedida."}), 200
    else:
        return jsonify({"message": "Erro ao abrir o stream RTSP."}), 500

@visualizer_cam.route('/stream', methods=['GET'])
def stream_video():
    """
    Endpoint para transmitir o vídeo RTSP como MJPEG.
    """
    global video_capture
    if video_capture is None or not video_capture.isOpened():
        return jsonify({"message": "O stream não foi inicializado. Use o endpoint '/simple' primeiro."}), 400

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@visualizer_cam.route('/stop', methods=['POST'])
def stop_stream():
    """
    Endpoint para encerrar o stream e liberar os recursos.
    """
    global video_capture, current_url
    try:
        if video_capture:
            video_capture.release()
            video_capture = None
            current_url = None  # Reseta a URL atual
            print("Stream encerrado com sucesso.")
            return jsonify({"message": "Stream encerrado com sucesso."}), 200
        else:
            return jsonify({"message": "Nenhum stream ativo para encerrar."}), 400
    except Exception as e:
        print(f"Erro ao encerrar o stream: {e}")
        return jsonify({"message": "Erro ao encerrar o stream."}), 500

