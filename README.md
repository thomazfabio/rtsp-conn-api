# 🎯 RTSP Conn System

<p align="left">
  <img src="https://img.shields.io/badge/Vue-3.x-brightgreen?logo=vue.js" alt="Vue.js" />
  <img src="https://img.shields.io/badge/Vuetify-3.x-1867C0?logo=vuetify&logoColor=white" alt="Vuetify" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/github/license/thomazfabio/rtsp-conn-system" alt="License" />
  <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow" alt="Status" />
</p>

---

## 🔍 Visão Geral

**RTSP Conn System** é um sistema completo para gerenciamento, visualização e análise de **streams de câmeras IP** via protocolo **RTSP/MJPEG**. Ele é dividido em dois módulos:

- 🎛️ **Front-End (Painel Web)** – Interface em Vue 3 + Vuetify para cadastro, visualização e controle das câmeras.
- 🚀 **Back-End (API RTSP Conn)** – API em FastAPI responsável por manipular os fluxos de vídeo, processar análises com IA e responder comandos.

---

## 🎯 Objetivo

Oferecer uma solução robusta e escalável para:

- Visualização em tempo real de câmeras RTSP
- Análise de vídeo via IA (ex: detecção de pessoas, objetos, comportamento)
- Painel de gerenciamento com cadastro de dispositivos
- Conectividade via API REST
- Extensibilidade para futuras integrações com sistemas de segurança e automação

---

## 🖼️ Demonstração

<p align="center">
  <img src="https://user-images.githubusercontent.com/123456789/rtsp-ui-demo.gif" alt="Demo UI" width="800" />
</p>

> *Interface web do painel com listagem das câmeras, visualização ao vivo e botões de controle.*

---

## 📁 Estrutura do Projeto

```bash
📦 rtsp-conn-system
 ┣ 📁 frontend/           # Interface web em Vue 3 + Vuetify
 ┃ ┣ 📁 src/
 ┃ ┗ 📄 package.json
 ┣ 📁 backend/            # API FastAPI para manipulação RTSP
 ┃ ┣ 📁 app/
 ┃ ┗ 📄 main.py
 ┣ 📄 README.md
 ┗ 📄 .env.example
```

---

## 🚀 Tecnologias

### 🔹 Frontend

- [Vue 3](https://vuejs.org/)
- [Vuetify 3](https://vuetifyjs.com/)
- [Pinia (State Management)](https://pinia.vuejs.org/)
- [Vite](https://vitejs.dev/)
- [Vue Router](https://router.vuejs.org/)

### 🔸 Backend

- [FastAPI](https://fastapi.tiangolo.com/)
- [uvicorn](https://www.uvicorn.org/) (ASGI server)
- [OpenCV](https://opencv.org/) para manipulação de vídeo
- [PyTorch](https://pytorch.org/) (opcional para IA)
- [Pydantic](https://docs.pydantic.dev/) para validação
- [Gunicorn](https://gunicorn.org/) (para produção)

---

## ⚙️ Instalação

### 1️⃣ Clone o projeto

```bash
git clone https://github.com/thomazfabio/rtsp-conn-system.git
cd rtsp-conn-system
```

### 2️⃣ Frontend

```bash
cd frontend
npm install        # ou yarn install
npm run dev        # inicia em http://localhost:3000
```

### 3️⃣ Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 🌐 Endpoints Principais

- `GET /cameras`: Lista todas as câmeras cadastradas
- `POST /cameras/start`: Inicia o stream de uma câmera
- `POST /cameras/stop`: Finaliza o stream de uma câmera
- `GET /stream/{camera_id}`: Acessa o vídeo da câmera (MJPEG)
- `GET /analytics`: Executa inferência usando IA (opcional)

Acesse a [documentação automática](http://localhost:8000/docs) do FastAPI.

---

## 🔐 Variáveis de Ambiente

Crie um `.env` na pasta `backend/` com base no `.env.example`:

```env
API_KEY=suachave123
RTSP_TIMEOUT=30
ENABLE_ANALYTICS=True
```

---

## 🧪 Testes

> *(em breve, cobertura com pytest + Vue Testing Library)*

---

## 📦 Build para Produção

### Frontend

```bash
npm run build
```

Os arquivos serão gerados em `dist/`, prontos para deploy com Nginx, Netlify, Vercel, etc.

### Backend

Recomendado: Gunicorn + Uvicorn em ambiente ASGI

```bash
gunicorn -k uvicorn.workers.UvicornWorker app.main:app
```

---

## 🧠 Roadmap

- [x] Visualização de streams RTSP
- [x] Gerenciador de câmeras via painel
- [ ] Integração com IA (detecção de pessoas/objetos)
- [ ] Alertas por evento
- [ ] Dashboard com gráficos
- [ ] Deploy com Docker

---

## 💬 Suporte

Entre em contato ou contribua através de:

- 📬 [GitHub Issues](https://github.com/thomazfabio/rtsp-conn-system/issues)
- 📘 [Discussões](https://github.com/thomazfabio/rtsp-conn-system/discussions)
- 📧 Email: thomaz.dev.contato@gmail.com

---

## 🤝 Contribuição

1. Faça um fork
2. Crie uma branch: `git checkout -b minha-feature`
3. Commit suas alterações: `git commit -m 'feat: nova feature'`
4. Push: `git push origin minha-feature`
5. Abra um Pull Request

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

---

<p align="center">Feito com 💚 por <a href="https://github.com/thomazfabio" target="_blank">Thomaz F.</a></p>
