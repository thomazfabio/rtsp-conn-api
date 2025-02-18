from flask import Blueprint, request, jsonify
from controllers import device_info_controller

device_info_bp = Blueprint('device_info_bp', __name__) # device_info_bp is the Blueprint name

@device_info_bp.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    return device_info_controller.create(data)

@device_info_bp.route('/update', methods=['PUT'])
def update():
    data = request.get_json()
    return jsonify({})

@device_info_bp.route('/delete', methods=['DELETE'])
def delete():
    id = request.args.get('id')
    return jsonify({})

@device_info_bp.route('/list_by_user_id', methods=['GET'])
def list():
    user_id = request.args.get('user_id')
    return jsonify({})

@device_info_bp.route('/get_all', methods=['GET'])
def get_all():
    return jsonify({})

@device_info_bp.route('/get_by_id', methods=['GET'])
def get_by_id():
    return jsonify({})
