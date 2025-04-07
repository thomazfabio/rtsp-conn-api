from flask import request, Response
from flask_restx import Namespace, Resource, fields
from controllers import stream_controller
import time

stream_manager = stream_controller.stream_manager

# Namespace RESTx
ns = Namespace('Stream', description='Gerenciamento de transmissões RTSP em tempo real')

# Models para documentação Swagger
start_model = ns.model('StartStreamModel', {
    'url_rtsp': fields.String(required=True, description='URL da câmera RTSP')
})

stop_model = ns.model('StopStreamModel', {
    'stream_id': fields.String(required=True, description='ID da stream ativa')
})

@ns.route('/start_stream')
class StartStream(Resource):
    @ns.expect(start_model)
    @ns.response(200, 'Stream iniciada com sucesso')
    @ns.response(400, 'JSON inválido ou URL ausente')
    @ns.response(500, 'Erro ao iniciar stream')
    def post(self):
        """Inicia uma nova transmissão RTSP"""
        data = request.get_json()
        if not data or "url_rtsp" not in data:
            return {"message": "JSON inválido ou URL ausente."}, 400

        url = data["url_rtsp"]
        success, stream_id = stream_manager.start_stream(url)

        if success:
            return {
                "message": "Stream iniciada com sucesso",
                "stream_id": stream_id,
                "stream_url": f"http://127.0.0.1:5000/stream/get_stream?stream_id={stream_id}"
            }, 200
        else:
            return {"message": stream_id}, 500

@ns.route('/stop_stream')
class StopStream(Resource):
    @ns.expect(stop_model)
    @ns.response(200, 'Stream parada com sucesso')
    @ns.response(400, 'JSON inválido ou stream_id ausente')
    @ns.response(404, 'Stream não encontrada')
    def post(self):
        """Encerra uma transmissão existente"""
        data = request.get_json()
        if not data or "stream_id" not in data:
            return {"message": "JSON inválido ou stream_id ausente."}, 400

        stream_id = data["stream_id"]
        success, message = stream_manager.stop_stream(stream_id)
        return {"message": message}, 200 if success else 404

@ns.route('/get_stream')
@ns.doc(params={'stream_id': 'ID da stream ativa'})
class GetStream(Resource):
    @ns.response(200, 'Transmissão de vídeo')
    @ns.response(400, 'stream_id ausente')
    @ns.response(404, 'Stream não encontrada')
    def get(self):
        """Transmite os frames da câmera via MJPEG"""
        stream_id = request.args.get("stream_id")
        if not stream_id:
            return {"message": "stream_id ausente."}, 400

        stream = stream_manager.get_stream(stream_id)
        if not stream:
            return {"message": "Stream não encontrada."}, 404

        def generate():
            fps_limit = 16  # Limitar a 16 FPS
            frame_interval = 1 / fps_limit
            last_frame_time = time.time()

            while True:
                frame = stream.get_frame()
                if frame:
                    current_time = time.time()
                    if current_time - last_frame_time >= frame_interval:
                        last_frame_time = current_time
                        yield (
                            b"--frame\r\n"
                            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                        )
                else:
                    time.sleep(0.1)  # Aguarda até que um frame esteja disponível

        return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")
