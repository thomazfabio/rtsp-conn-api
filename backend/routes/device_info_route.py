from flask_restx import Namespace, Resource, fields
from flask import request
from controllers import device_info_controller

# Criação do Namespace
ns = Namespace('Manage Device Info', description='Operações relacionadas aos dispositivos')

# Modelo para criação/atualização (exemplo — pode ser ajustado conforme seu schema)
device_model = ns.model('DeviceCreate', {
    'id': fields.Integer(description='ID do modelo de dispositivo'),
    'tipo': fields.String(description='Tipo do dispositivo (ex: câmera, NVR, etc)'),
    'fabricante': fields.String(description='Fabricante do dispositivo'),
    'modelo': fields.String(description='Modelo do dispositivo'),
    'path_rtsp': fields.String(description='Caminho RTSP padrão (ex: /live.sdp)'),
    'versao': fields.String(description='Versão do dispositivo ou firmware'),
    # Adicione mais campos aqui conforme necessário
})

# Rota: Criar dispositivo
@ns.route('/create')
class CreateDevice(Resource):
    @ns.expect(device_model)
    @ns.doc(description="Cria um novo dispositivo (base para a câmera).")
    def post(self):
        data = request.get_json()
        return device_info_controller.create(data)


# Rota: Atualizar dispositivo
@ns.route('/update')
class UpdateDevice(Resource):
    @ns.expect(device_model)
    @ns.doc(description="Atualiza as informações de um dispositivo.")
    def put(self):
        data = request.get_json()
        return device_info_controller.update(data)


# Rota: Deletar dispositivo por ID (query param)
@ns.route('/delete')
class DeleteDevice(Resource):
    @ns.doc(params={'id': 'ID do dispositivo a ser deletado'})
    def delete(self):
        id = request.args.get('id')
        return device_info_controller.delete(id)


# Rota: Buscar todos os dispositivos
@ns.route('/get_all')
class GetAllDevices(Resource):
    @ns.doc(description="Retorna todos os dispositivos cadastrados.")
    def get(self):
        return device_info_controller.get_all()


# Rota: Buscar dispositivo por ID
@ns.route('/get_by_id')
class GetDeviceById(Resource):
    @ns.doc(params={'id': 'ID do dispositivo'}, description="Busca um dispositivo pelo ID.")
    def get(self):
        id = request.args.get('id')
        return device_info_controller.get_by_id(id)


# Rota: Buscar dispositivo por tipo
@ns.route('/get_by_type')
class GetDeviceByType(Resource):
    @ns.doc(params={'device_tipo': 'Tipo do dispositivo'}, description="Busca dispositivos por tipo.")
    def get(self):
        tipo = request.args.get('device_tipo')
        return device_info_controller.get_by_type(tipo)

# Exporta o namespace para ser adicionado na API principal
api = ns
