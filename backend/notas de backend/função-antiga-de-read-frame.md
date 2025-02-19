def _read_frames(self):
        while self.running:
            with self.lock:
                if not self.running:
                    break
                ret, frame = self.capture.read()
                # Aqui você pode adicionar o processamento de imagem
                # antes de adicionar o frame ao buffer
                # reddimensionar
                frame = cv2.resize(frame, (640, 480))

            if not ret:
                print(
                    f"Erro: Não foi possível ler o frame do stream {
                        self.url}."
                )
                time.sleep(2)  # Pausa antes de tentar novamente
                continue
            # Adiciona o frame ao buffer
            ret, buffer = cv2.imencode(".jpg", frame)
            if ret:
                self.buffer.append(buffer.tobytes())
            time.sleep(0.0)  # Controla o consumo de CPU (ajustável)