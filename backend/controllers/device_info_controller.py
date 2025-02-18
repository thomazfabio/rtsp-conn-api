from flask import jsonify
from model import device_info_model
from database import db

def create(data):

    try:
        new_device_info = device_info_model.DeviceInfo(
            fabricante = data["fabricante"],
            modelo = data["modelo"],
            path_rtsp = data["path_rtsp"],
            versao = data["versao"]
            
        )
        db.session.add(new_device_info)
        db.session.commit()
        return jsonify({"message": "Device info created successfully!"}), 201
    except Exception as e:
        return jsonify({"message": f"Error creating device info: {e}"}), 500
    
def get_all():
    try:
        device_info = device_info_model.DeviceInfo.query.all()
        return jsonify([device_info.serialize() for device_info in device_info])
    except Exception as e:
        return jsonify({"message": f"Error getting device info: {e}"}), 500
    
def get_by_id(id):
    try:
        device_info = device_info_model.DeviceInfo.query.get(id)
        if device_info:
            return jsonify(device_info.serialize())
        return jsonify({"message": "Device info not found"}), 404
    except Exception as e:
        return jsonify({"message": f"Error getting device info: {e}"}), 500
    
def update(data):
    try:
        device_info = device_info_model.DeviceInfo.query.get(data["id"])
        if device_info:
            device_info.fabricante = data["fabricante"]
            device_info.modelo = data["modelo"]
            device_info.path_rtsp = data["path_rtsp"]
            device_info.versao = data["versao"]
            db.session.commit()
            return jsonify({"message": "Device info updated successfully!"})
        return jsonify({"message": "Device info not found"}), 404
    except Exception as e:
        return jsonify({"message": f"Error updating device info: {e}"}), 500
    
def delete(id):
    try:
        device_info = device_info_model.DeviceInfo.query.get(id)
        if device_info:
            db.session.delete(device_info)
            db.session.commit()
            return jsonify({"message": "Device info deleted successfully!"})
        return jsonify({"message": "Device info not found"}), 404
    except Exception as e:
        return jsonify({"message": f"Error deleting device info: {e}"}), 500
    