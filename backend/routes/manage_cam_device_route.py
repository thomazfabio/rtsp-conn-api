from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from controllers import manage_cam_device_controller

ns = Namespace('Manage Cam Device', description='Gerenciamento dos dispositivos de câmera')

# Models de entrada (apenas exemplos básicos para Swagger; podem ser aprimorados)
device_model = ns.model('Device', {
    'id': fields.Integer(description='ID do registro'),
    'user_id': fields.Integer(description='ID do usuário'),
    'device_id': fields.Integer(description='ID do dispositivo (FK para device_info.id)'),
    'cam_name': fields.String(description='Nome da câmera'),
    'grupo': fields.String(description='Grupo da câmera (opcional)'),
    'full_cam_url_stream': fields.String(description='URL completa para acesso à câmera via stream'),
    'full_cam_url_rtsp': fields.String(description='URL completa para acesso à câmera via RTSP'),
    'cam_status': fields.String(description='Status da câmera (online, offline, error)'),
    'device_config': fields.Raw(description='Configurações adicionais do dispositivo em JSON'),
    'created_at': fields.DateTime(description='Data de criação'),
    'updated_at': fields.DateTime(description='Data da última atualização'),
})

@ns.route('/create')
class CreateDevice(Resource):
    @ns.expect(device_model)
    @ns.response(200, 'Dispositivo criado')
    def post(self):
        """Cria um novo dispositivo (cãmera)"""
        data = request.get_json()
        resp = manage_cam_device_controller.create(data)
        return resp[0].get_json(), resp[1]


@ns.route('/update')
class UpdateDevice(Resource):
    @ns.expect(device_model)
    @ns.response(200, 'Dispositivo atualizado')
    def put(self):
        """Atualiza um dispositivo existente"""
        data = request.get_json()
        resp = manage_cam_device_controller.update(data)
        return resp[0].get_json(), resp[1]


@ns.route('/delete')
@ns.doc(params={'id': 'ID do dispositivo a ser deletado'})
class DeleteDevice(Resource):
    @ns.response(200, 'Dispositivo deletado')
    def delete(self):
        """Deleta um dispositivo pelo ID"""
        id = request.args.get('id')
        resp = manage_cam_device_controller.delete(id)
        return resp[0].get_json(), resp[1]


@ns.route('/list_by_user_id')
@ns.doc(params={'user_id': 'ID do usuário'})
class ListDevices(Resource):
    @ns.response(200, 'Lista de dispositivos')
    def get(self):
        """Lista dispositivos por ID de usuário"""
        user_id = request.args.get('user_id')
        resp = manage_cam_device_controller.getByUserId(user_id)
        return resp[0].get_json(), resp[1]


@ns.route('/get')
class GetStub(Resource):
    @ns.response(200, 'Retorna dicionário vazio')
    def get(self):
        """Retorna objeto vazio (stub)"""
        return {}, 200


@ns.route('/get_by_id')
class GetByIdStub(Resource):
    @ns.response(200, 'Retorna dicionário vazio')
    def get(self):
        """Retorna objeto vazio (stub)"""
        return {}, 200
