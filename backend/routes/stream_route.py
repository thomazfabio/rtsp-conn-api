from flask import Blueprint, jsonify, request, Response
from controllers import stream_controller
import time

stream_manager = stream_controller.stream_manager

stream = Blueprint("stream_manager", __name__)

@stream.route("/start_stream", methods=["POST"])
def start_stream():
    data = request.get_json()
    if not data or "url_rtsp" not in data:
        return jsonify({"message": "JSON inválido ou URL ausente."}), 400

    url = data["url_rtsp"]
    success, stream_id = stream_manager.start_stream(url)

    if success:
        return jsonify({
            "message": "Stream iniciado com sucesso",
            "stream_id": stream_id,
            "stream_url": f"http://127.0.0.1:5000/stream/get_stream?stream_id={stream_id}"
        }), 200
    else:
        return jsonify({"message": stream_id}), 500



@stream.route("/stop_stream", methods=["POST"])
def stop_stream():
    data = request.get_json()
    if not data or "stream_id" not in data:
        return jsonify({"message": "JSON inválido ou stream_id ausente."}), 400

    stream_id = data["stream_id"]
    success, message = stream_manager.stop_stream(stream_id)
    return jsonify({"message": message}), 200 if success else 404



@stream.route("/get_stream", methods=["GET"])
def stream_video():
    stream_id = request.args.get("stream_id")
    if not stream_id:
        return jsonify({"message": "stream_id ausente."}), 400

    stream = stream_manager.get_stream(stream_id)
    if not stream:
        return jsonify({"message": "Stream não encontrado."}), 404

    def generate():
        fps_limit = 16  # Limitar a 10 frames por segundo (ajustável)
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