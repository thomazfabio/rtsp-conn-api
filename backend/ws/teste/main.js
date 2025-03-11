// Conectando ao servidor WebSocket
const socket = io("http://localhost:5000");

// Enviar evento de conexão
socket.emit("conectar");

// Escutar resposta do servidor
socket.on("conectado", function (data) {
  console.log("Servidor:", data.msg);
});

