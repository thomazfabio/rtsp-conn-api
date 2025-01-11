from flask import jsonify, request
from . import add_url_rtsp  # Importando o Blueprint definido no __init__.py
from rtsp_core import test_url_rtsp

@add_url_rtsp.route('/create', methods=['POST'])
def create():

    #obter json enviado no corpo da requisição
    data = request.get_json()

    if not data:
        return jsonify({"message": "JSON inválido"}), 400

    print(data)
    print(type(data))

    # montando url rtsp
    if data['protocol'] == 'rtsp':
        url_rtsp = f"rtsp://{data['device_user']}:{data['device_pass']}@{data['ip']}:{data['port']}/{data['path']}?{data['channel']}&{data['subtype']}"
    else:
        return jsonify({"message": "Protocolo inválido"}), 400
    
    # Testando a URL RTSP
    sucess = test_url_rtsp.test_url_rtsp(url_rtsp)
    if not sucess:
        print("Error: Could not open video.")
    else:
        print("Success: Video opened.")
    # Exemplo de rota para criar uma URL RTSP
    return url_rtsp, 200