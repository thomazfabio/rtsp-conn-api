from flask import Blueprint, request, jsonify
from controllers import manage_cam_device_controller

manage_cam_device_bp = Blueprint('manage_cam_device_bp', __name__) # manage_cam_device_bp is the Blueprint name

@manage_cam_device_bp.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    return manage_cam_device_controller.create(data)
    

@manage_cam_device_bp.route('/update', methods=['PUT'])
def update():
    data = request.get_json()
    return manage_cam_device_controller.update(data)

@manage_cam_device_bp.route('/delete', methods=['DELETE'])
def delete():
    id = request.args.get('id')
    return manage_cam_device_controller.delete(id)

@manage_cam_device_bp.route('/list_by_user_id', methods=['GET'])
def list():
    user_id = request.args.get('user_id')
    return manage_cam_device_controller.getByUserId(user_id)

@manage_cam_device_bp.route('/get', methods=['GET'])
def get():
    return jsonify({})

@manage_cam_device_bp.route('/get_by_id', methods=['GET'])
def get_by_id():
    return jsonify({})
