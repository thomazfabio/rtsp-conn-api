# 🎛️ Painel de Gerenciamento de Câmeras – RTSP Conn Panel

![License](https://img.shields.io/github/license/thomazfabio/rtsp-conn-panel?color=blue)
![GitHub last commit](https://img.shields.io/github/last-commit/thomazfabio/rtsp-conn-panel)
![GitHub issues](https://img.shields.io/github/issues/thomazfabio/rtsp-conn-panel)
![Vue.js](https://img.shields.io/badge/Vue-3.x-brightgreen)
![Vuetify](https://img.shields.io/badge/Vuetify-3.x-1867C0?logo=vuetify&logoColor=white)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

---

## 📌 Descrição

Este projeto é uma interface moderna desenvolvida com **Vue 3** + **Vuetify 3** para gerenciar câmeras IP e fluxos de vídeo RTSP/MJPEG. O painel conecta-se à API [RTSP Conn](https://thomazfabio.github.io/rtsp-conn-api/) para iniciar, listar e monitorar transmissões de vídeo em tempo real.

---

## ❗️ Links Úteis

- 📘 [Documentação da API Backend](https://thomazfabio.github.io/rtsp-conn-api/)
- 🐛 [Relatar Problemas](https://github.com/thomazfabio/rtsp-conn-panel/issues)
- 💬 [Back-end API (Repositório)](https://github.com/thomazfabio/rtsp-conn-api)
- 🧩 [Vuetify Docs](https://vuetifyjs.com/)
- 🎮 [Vuetify Playground](https://play.vuetifyjs.com/)
- 💬 [Comunidade Vuetify (Discord)](https://community.vuetifyjs.com/)

---

## ✨ Funcionalidades

- 🎥 Visualização de streams RTSP/MJPEG em tempo real
- 📡 Início/parada de transmissões conectadas à API
- ➕ Cadastro e edição de câmeras com campos personalizados
- 🧠 Suporte a análises inteligentes via back-end com IA
- 🗂️ Interface intuitiva com layout responsivo
- 📝 Logs de eventos e estados da conexão em tempo real

---

## 🛠️ Tecnologias Utilizadas

- [Vue 3](https://vuejs.org/)
- [Vuetify 3](https://vuetifyjs.com/)
- [Pinia](https://pinia.vuejs.org/)
- [Vue Router](https://router.vuejs.org/)
- [Vite](https://vitejs.dev/)
- [vite-plugin-vue-layouts](https://github.com/JohnCampionJr/vite-plugin-vue-layouts)
- [unplugin-vue-components](https://github.com/antfu/unplugin-vue-components)

---

## 💿 Instalação

Clone o repositório e instale as dependências com o gerenciador de sua escolha:

```bash
git clone https://github.com/thomazfabio/rtsp-conn-panel.git
cd rtsp-conn-panel
```

| Gerenciador de Pacotes | Comando        |
|------------------------|----------------|
| npm                    | `npm install`  |
| yarn                   | `yarn install` |
| pnpm                   | `pnpm install` |
| bun                    | `bun install`  |

> Após isso, o ambiente estará pronto para desenvolvimento.

---

## ▶️ Executando em Desenvolvimento

Para iniciar o servidor de desenvolvimento local:

```bash
npm run dev
```

> Acesse em: [http://localhost:3000](http://localhost:3000)

⚠️ Para suprimir warnings de importação JSON do Vuetify, adicione:

```bash
NODE_OPTIONS='--no-warnings'
```

Se estiver usando Node 21.3.0 ou superior:

```bash
NODE_OPTIONS='--disable-warning=5401'
```

---

## 📦 Build para Produção

```bash
npm run build
```

> A versão otimizada será gerada na pasta `dist/`.

---

## 📂 Estrutura do Projeto

```
📁 src
 ┣ 📁 components        → Componentes Vue reutilizáveis
 ┣ 📁 layouts           → Layouts dinâmicos com vue-layouts
 ┣ 📁 pages             → Rotas e páginas principais
 ┣ 📁 plugins           → Plugins e configurações
 ┣ 📁 stores            → Estados gerenciados pelo Pinia
 ┣ 📁 utils             → Funções utilitárias
 ┣ 📄 App.vue
 ┗ 📄 main.ts
```

---

## 💪 Apoie o Vuetify

Este projeto é construído sobre o Vuetify, um projeto open source mantido com apoio da comunidade.

- 💼 [Solicite Suporte Empresarial](https://support.vuetifyjs.com/)
- ⭐️ [Patrocine no GitHub](https://github.com/sponsors/johnleider)
- 🤝 [Apoie via OpenCollective](https://opencollective.com/vuetify)
- ❤️ [Doe no Patreon](https://www.patreon.com/vuetify)

---

## 🧩 Agradecimentos

- [@vuetifyjs](https://github.com/vuetifyjs) pela incrível UI library
- [@johnleider](https://github.com/johnleider) e toda a equipe por manter o Vuetify
- [Vue.js Team](https://github.com/vuejs/core)
- Comunidade Vue/Vuetify por pacotes e suporte

---

## 📑 Licença

Distribuído sob a licença [MIT](https://opensource.org/licenses/MIT).

---

**Desenvolvido com ❤️ por [@thomazfabio](https://github.com/thomazfabio)**
