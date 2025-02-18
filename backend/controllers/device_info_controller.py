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