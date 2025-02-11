import cv2
import face_recognition
import numpy as np
import sqlite3
import threading
import time

# Lista de URLs RTSP
RTSP_STREAMS = [
    "rtsp://usuario:senha@ip_camera1:porta/stream",
    "rtsp://usuario:senha@ip_camera2:porta/stream"
]

# Conectar ao banco e carregar embeddings dos rostos conhecidos
def carregar_rostos():
    conn = sqlite3.connect("face_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT name, encoding FROM faces")
    known_faces = cursor.fetchall()
    conn.close()

    known_names = []
    known_encodings = []

    for name, encoding_blob in known_faces:
        encoding_array = np.frombuffer(encoding_blob, dtype=np.float64)
        known_names.append(name)
        known_encodings.append(encoding_array)

    return known_names, known_encodings

# Função para processar RTSP em paralelo
def processar_rtsp(rtsp_url, known_names, known_encodings):
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print(f"Erro ao abrir {rtsp_url}")
        return

    while True:
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            print(f"Erro ao capturar frame de {rtsp_url}")
            continue

        # Redimensionar para 640x480 para otimizar processamento
        frame = cv2.resize(frame, (640, 480))

        # Converter para RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detectar rostos
        face_locations = face_recognition.face_locations(rgb_frame, model="cnn")  # Mude para "hog" para CPU
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Comparar cada rosto detectado
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            results = face_recognition.compare_faces(known_encodings, face_encoding)
            distances = face_recognition.face_distance(known_encodings, face_encoding)

            name = "Desconhecido"
            if any(results):
                best_match_index = np.argmin(distances)
                name = known_names[best_match_index]

            # Exibir nome detectado
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Log de detecção
            print(f"[{rtsp_url}] Rosto detectado: {name}")

        # Mostrar o vídeo processado (pode ser removido para rodar apenas em background)
        cv2.imshow(f"RTSP {rtsp_url}", frame)

        # Processa 1 frame por segundo
        elapsed_time = time.time() - start_time
        time.sleep(max(1.0 - elapsed_time, 0))

        # Pressione 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Carregar rostos conhecidos antes de iniciar os threads
known_names, known_encodings = carregar_rostos()

# Criar threads para múltiplos streams RTSP
threads = []
for rtsp_url in RTSP_STREAMS:
    t = threading.Thread(target=processar_rtsp, args=(rtsp_url, known_names, known_encodings))
    t.start()
    threads.append(t)

# Aguardar todas as threads finalizarem
for t in threads:
    t.join()
