from flask import Blueprint, request, jsonify
from controllers import manage_cam_device_controller

manage_cam_device_bp = Blueprint('manage_cam_device_bp', __name__) # manage_cam_device_bp is the Blueprint name

@manage_cam_device_bp.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    return manage_cam_device_controller.create(data)
    

@manage_cam_device_bp.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    return jsonify(data)

@manage_cam_device_bp.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    return jsonify(data)

@manage_cam_device_bp.route('/list', methods=['GET'])
def list():
    return jsonify([])

@manage_cam_device_bp.route('/get', methods=['GET'])
def get():
    return jsonify({})

@manage_cam_device_bp.route('/get_by_id', methods=['GET'])
def get_by_id():
    return jsonify({})
