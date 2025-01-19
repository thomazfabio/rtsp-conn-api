import subprocess
from flask import Flask, jsonify,request
from . import visualizer_cam


@visualizer_cam.route('/simple', methods=['POST'])
def simple():
    rtsp_url = request.get_json()['url']

    # Comando para FFmpeg (transcodifica RTSP para HLS)
    command = [
        "ffmpeg",
        "-i", rtsp_url,             # Entrada RTSP
        "-c:v", "libx264",          # Codec de vídeo
        "-preset", "veryfast",      # Configuração de transcodificação
        "-f", "hls",                # Formato de saída
        "-hls_time", "1",           # Duração de cada segmento HLS
        "-hls_list_size", "3",      # Quantos segmentos manter na lista
        "-hls_flags", "delete_segments",  # Apaga segmentos antigos
        "stream/simple/simple_stream.m3u8"        # Arquivo HLS gerado
    ]

    # Inicia o processo FFmpeg
    subprocess.Popen(command)

    # Retorna a URL do stream HLS
    return jsonify({"stream_url": "http://localhost:5000/stream/simple/simple_stream.m3u8"}), 200


