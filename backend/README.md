# 🎥 RTSP-Conn API – Gerenciador de Streaming com Flask + OpenCV

> Backend para gerenciamento de câmeras e streaming de vídeo via **RTSP**, com proxy para MJPEG via HTTP. Ideal para sistemas de **visão computacional** e monitoramento inteligente.

---

## 🌐 Visão Geral

Este projeto é uma **API de gerenciamento de vídeo** construída com **Flask** e **OpenCV**, capaz de:

✅ Registrar e armazenar câmeras com URL RTSP  
✅ Iniciar transmissões em MJPEG via HTTP  
✅ Gerenciar múltiplos fluxos simultâneos com threads  
✅ Servir como **proxy de vídeo** para dispositivos DVR, IP Cams, NVRs, entre outros  
✅ Pronto para futuras integrações com **servidores de inferência IA**

---

## 📡 Funcionalidades

- **Registrar câmeras**: Armazena informações detalhadas das câmeras conectadas.
- **Iniciar streaming**: Conecta-se ao RTSP e retorna o MJPEG via HTTP.
- **Transmissão nativa**: Sem necessidade de players ou plugins externos.
- **Gerenciamento via API REST**: Com endpoints organizados e documentados.
- **Thread-safe (em 1 worker)**: Cada fluxo de vídeo roda em sua própria thread.
- **Compatível com múltiplos dispositivos**: Câmeras IP, DVRs, URLs RTSP diretas.

---

## 🔗 Documentação da API

Acesse a documentação completa da API aqui:  
📄 **[https://thomazfabio.github.io/rtsp-conn-api/](https://thomazfabio.github.io/rtsp-conn-api/)**

---

## 🚀 Como Usar

### ▶️ 1. Criar uma nova câmera

**Endpoint:** `POST /manage_cam_device/create`  
**Exemplo de payload:**

```json
{
  "id": 0,
  "user_id": 0,
  "device_id": 0,
  "cam_name": "Camera Piscina",
  "grupo": "Residencial",
  "full_cam_url_stream": "http://ip_da_api/video_feed/1",
  "full_cam_url_rtsp": "rtsp://usuario:senha@ip:porta/caminho",
  "cam_status": "ativa",
  "device_config": {},
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

ℹ️ Consulte a [documentação oficial](https://thomazfabio.github.io/rtsp-conn-api/) para detalhes completos sobre esse endpoint.

---

### 🎬 2. Iniciar um streaming

**Endpoint:** `POST /stream/start_stream`  
**Payload:**

```json
{
  "url_rtsp": "rtsp://usuario:senha@ip:porta/caminho"
}
```

O retorno será uma **URL HTTP** com o fluxo de vídeo no formato MJPEG. Exemplo:

```
http://localhost:5000/video_feed/1
```

---

## ⚙️ Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/rtsp-conn-api.git
cd rtsp-conn-api
```

### 2. Criar ambiente virtual (opcional)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

## 🏁 Execução em Produção (recomendado)

Execute com **Gunicorn** para melhor performance e gerenciamento:

```bash
gunicorn --workers 1 --threads 200 -b 0.0.0.0:5000 app:app
```

⚠️ **Importante:**  
Use **apenas 1 worker**. O sistema utiliza `threads` para gerenciar as transmissões e ainda **não possui sincronização entre múltiplos processos**. Caso use mais de 1 worker, as threads de diferentes processos **não compartilharão estado**, podendo causar inconsistências.

🔧 Se for necessário usar múltiplos workers ou instâncias em produção, considere implementar sua própria solução de **sincronização de estado**. Algumas sugestões:

- Armazenamento centralizado em **Redis**, **banco de dados relacional** ou **MongoDB**
- Uso de serviços como **RabbitMQ** ou **Kafka** para controle de eventos entre processos
- Criação de microsserviços independentes para cada fluxo

---
## 📦 Tecnologias Utilizadas

| Tecnologia | Função |
|------------|--------|
| <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="20"/>  Python   | Linguagem base |
| <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" height="20"/>  Flask    | Framework web backend |
| <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/opencv/opencv-original.svg" height="20"/>  OpenCV   | Captura e processamento de vídeo |
| <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg" height="20"/>  Gunicorn | Servidor WSGI para produção |
| <img src="https://cdn-icons-png.flaticon.com/512/833/833314.png" height="20"/>  MJPEG    | Transmissão leve via HTTP |

---

## 🧠 Futuro do Projeto

Este gerenciador de streaming faz parte de um sistema maior de **visão computacional**, e em breve contará com:

- Envio de frames para servidores de **inferência em IA**
- Integração com **WebSockets** para transmissão em tempo real
- Suporte a múltiplos usuários e permissões
- Interface web para visualização e controle das câmeras

---

## 🤝 Contribuições

Sinta-se à vontade para abrir issues, relatar bugs, sugerir melhorias ou enviar pull requests. Toda contribuição é bem-vinda! 🚀
