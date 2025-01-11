from flask import jsonify, request
from . import add_url_rtsp  # Importando o Blueprint definido no __init__.py
from rtsp_core import test_url_rtsp
from extensions.extensions import db
from .models import UrlRtsp

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
        mounted_url_rtsp = f"rtsp://{data['device_user']}:{data['device_pass']}@{data['ip']}:{data['port']}/{data['path']}?{data['channel']}&{data['subtype']}"

        url_rtsp = UrlRtsp(
            user_id=data['user_id'],
            url=mounted_url_rtsp,
            group=data['group'],
            channel=data['channel'],
            name=data['name']
        )

        # Adiciona o objeto à sessão
        db.session.add(url_rtsp)

        # Salva as mudanças no banco de dados
        db.session.commit()
        
    else:
        return jsonify({"message": "Protocolo inválido"}), 400
    
    # Testando a URL RTSP
    sucess = test_url_rtsp.test_url_rtsp(mounted_url_rtsp)
    if not sucess:
        print("Error: Could not open video.")
    else:
        print("Success: Video opened.")
    # Exemplo de rota para criar uma URL RTSP
    return mounted_url_rtsp, 200

# Rota para listar todas as URLs RTSP
@add_url_rtsp.route('/list-all', methods=['GET'])
def list():
    urls = db.session.query(UrlRtsp).all()
    # Converte a lista de objetos em um formato de dicionário
    urls_data = []
    for url in urls:
        urls_data.append({
            "id": url.id,
            "user_id": url.user_id,
            "url": url.url,
            "group": url.group,
            "channel": url.channel,
            "name": url.name
        })
    
    # Retorna os dados no formato JSON
    return jsonify(urls_data), 200

# Rota para listar uma URL RTSP específica
@add_url_rtsp.route('/list/<int:id>', methods=['GET'])
def list_one(id):
    url = db.session.query(UrlRtsp).filter(UrlRtsp.id == id).first()
    if not url:
        return jsonify({"message": "URL RTSP não encontrada"}), 404
    
    # Converte o objeto em um formato de dicionário
    url_data = {
        "id": url.id,
        "user_id": url.user_id,
        "url": url.url,
        "group": url.group,
        "channel": url.channel,
        "name": url.name
    }

    # Retorna os dados no formato JSON
    return jsonify(url_data), 200

# Rota para deletar uma URL RTSP específica
@add_url_rtsp.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    url = db.session.query(UrlRtsp).filter(UrlRtsp.id == id).first()
    if not url:
        return jsonify({"message": "URL RTSP não encontrada"}), 404
    
    # Deleta o objeto da sessão
    db.session.delete(url)

    # Salva as mudanças no banco de dados
    db.session.commit()

    return jsonify({"message": "URL RTSP deletada com sucesso"}), 200

# Rota para atualizar uma URL RTSP específica
@add_url_rtsp.route('/update/<int:id>', methods=['PUT'])
def update(id):
    url = db.session.query(UrlRtsp).filter(UrlRtsp.id == id).first()
    if not url:
        return jsonify({"message": "URL RTSP não encontrada"}), 404

    #obter json enviado no corpo da requisição
    data = request.get_json()

    if not data:
        return jsonify({"message": "JSON inválido"}), 400

    # montando url rtsp
    if data['protocol'] == 'rtsp':
        mounted_url_rtsp = f"rtsp://{data['device_user']}:{data['device_pass']}@{data['ip']}:{data['port']}/{data['path']}?{data['channel']}&{data['subtype']}"
        url.url = mounted_url_rtsp
        url.group = data['group']
        url.channel = data['channel']
        url.name = data['name']

        # Salva as mudanças no banco de dados
        db.session.commit()
        
    else:
        return jsonify({"message": "Protocolo inválido"}), 400
    
    # Testando a URL RTSP
    sucess = test_url_rtsp.test_url_rtsp(mounted_url_rtsp)
    if not sucess:
        print("Error: Could not open video.")
    else:
        print("Success: Video opened.")
    # Exemplo de rota para criar uma URL RTSP
    return mounted_url_rtsp, 200