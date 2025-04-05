from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields, Api
from controllers import services_controller

# Criação do Blueprint
#url_rtsp_bp = Blueprint('url_rtsp_bp', __name__)

# Criação da API e Namespace RESTx
ns = Namespace('Services', description='Funcionalidades de serviços da API')

# Modelo para documentação Swagger
url_model = ns.model('UrlModel', {
    'url': fields.String(required=True, description='URL da câmera RTSP')
})

@ns.route('/teste_url')
class TesteUrl(Resource):
    @ns.doc(
        description="Endpoint para testar a conexão com uma URL RTSP.",
        responses={
            200: "Retorna status 'online' se a URL for acessível ou 'error' se falhar."
        },
        tags=['Teste da URL RTSP'])
    @ns.expect(url_model)
    def post(self):
        data = request.get_json()
        url_rtsp = data['url']
        success = services_controller.test_url_rtsp(url_rtsp)
        return {"status": "online" if success else "error"}, 200

# Importante: a Api (Api(url_rtsp_bp)) deve ser criada em outro lugar ou aqui dentro se desejar documentação separada


api = ns
