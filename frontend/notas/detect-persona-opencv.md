O OpenCV possui métodos e modelos pré-treinados para detectar pessoas, além de faces. A detecção de pessoas pode ser realizada usando o **detector de HOG (Histogram of Oriented Gradients)** ou redes neurais como **MobileNet SSD**, ambas disponíveis no OpenCV.

### Métodos disponíveis para detectar pessoas no OpenCV:

#### 1. **Detecção de Pessoas com HOG + SVM (predefinição do OpenCV)**
O OpenCV possui um detector HOG otimizado com um classificador SVM pré-treinado para detectar pedestres.

**Exemplo de código para detectar pessoas:**
```python
import cv2

# Inicializar o detector de HOG
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Ler a imagem ou vídeo
image = cv2.imread("people.jpg")

# Detectar pessoas
boxes, weights = hog.detectMultiScale(image, winStride=(8, 8), padding=(8, 8), scale=1.05)

# Desenhar os retângulos ao redor das pessoas detectadas
for (x, y, w, h) in boxes:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Exibir o resultado
cv2.imshow("Pessoas Detectadas", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

**Parâmetros Importantes:**
- `winStride`: Define o tamanho do deslocamento da janela deslizante.
- `padding`: Preenchimento em torno da janela para melhorar a detecção.
- `scale`: Fator de escala usado para o redimensionamento da imagem.

**Vantagem**:
- Simples e rápido de usar para aplicações básicas.

**Desvantagem**:
- Menor precisão em comparação com redes neurais.

---

#### 2. **Detecção de Pessoas com Redes Neurais Pré-Treinadas (MobileNet SSD ou YOLO)**
Se você precisa de mais precisão, pode usar redes neurais pré-treinadas, como **MobileNet SSD** ou **YOLO**. O OpenCV suporta redes através do módulo `cv2.dnn`.

**Exemplo com MobileNet SSD:**
```python
import cv2

# Carregar o modelo e as configurações
net = cv2.dnn.readNetFromCaffe(
    "MobileNetSSD_deploy.prototxt",
    "MobileNetSSD_deploy.caffemodel"
)

# Classes suportadas (pessoas têm o índice 15 neste modelo)
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant",
           "sheep", "sofa", "train", "tvmonitor"]

# Ler a imagem
image = cv2.imread("people.jpg")
(h, w) = image.shape[:2]

# Pré-processar a imagem para a rede
blob = cv2.dnn.blobFromImage(image, 0.007843, (300, 300), 127.5)
net.setInput(blob)

# Fazer a inferência
detections = net.forward()

# Processar as detecções
for i in range(detections.shape[2]):
    confidence = detections[0, 0, i, 2]
    if confidence > 0.5:  # Ajustar o limiar de confiança
        idx = int(detections[0, 0, i, 1])
        if CLASSES[idx] == "person":  # Apenas pessoas
            box = detections[0, 0, i, 3:7] * [w, h, w, h]
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)

# Mostrar a imagem com pessoas detectadas
cv2.imshow("Pessoas Detectadas", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

**Vantagem**:
- Mais preciso que o HOG para detectar pessoas em diferentes cenários.

**Desvantagem**:
- Um pouco mais lento, dependendo do hardware.

---

#### 3. **Detecção de Pessoas com YOLO (You Only Look Once)**
O YOLO é outra alternativa muito popular, suportada pelo OpenCV via `cv2.dnn`.

Se precisar de um exemplo com YOLO, me avise que eu explico como configurá-lo.

---

### Comparação entre HOG e Redes Neurais:
| Método               | Vantagem                              | Desvantagem                      |
|----------------------|---------------------------------------|----------------------------------|
| **HOG + SVM**        | Simples, eficiente em cenários básicos | Menor precisão em casos complexos |
| **MobileNet SSD**    | Boa precisão, mais leve que YOLO      | Requer mais configuração         |
| **YOLO (v4/v5/v8)**  | Altíssima precisão                   | Mais pesado, depende de hardware |

Escolha o método dependendo do seu caso de uso (simples ou avançado) e do hardware disponível. Se precisar de ajuda para configurar algum dos métodos, posso detalhar!