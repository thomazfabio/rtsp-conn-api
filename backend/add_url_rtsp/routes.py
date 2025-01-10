from flask import jsonify, request
from . import add_url_rtsp  # Importando o Blueprint definido no __init__.py

@add_url_rtsp.route('/create', methods=['POST'])
def create():

    #obter json enviado no corpo da requisição
    data = request.get_json()

    if not data:
        return jsonify({"message": "JSON inválido"}), 400

    print(data)
    # Exemplo de rota para criar uma URL RTSP
    return jsonify(data), 200