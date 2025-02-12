from flask import jsonify
from model import manage_cam_device_model
from database import db


def create(data):

    try:
        new_cam_device = manage_cam_device_model.ManageCamDevice(
            user_id=data.get("user_id"),
            device_id=data.get("device_id"),
            cam_name=data.get("cam_name"),
            grupo=data.get("grupo"),
            full_cam_url_stream=data.get("full_cam_url_stream"),
            full_cam_url_rtsp=data.get("full_cam_url_rtsp"),
            cam_status=data.get("cam_status"),
            device_config=data.get("device_config"),
        )
        db.session.add(new_cam_device)
        db.session.commit()
        return jsonify({"message": "Cam device created successfully!"}), 201
    except Exception as e:
        return jsonify({"message": f"Error creating cam device: {e}"}), 500


def getAll():
    try:
        cam_devices = manage_cam_device_model.ManageCamDevice.query.all()
        return jsonify([cam_device.serialize() for cam_device in cam_devices]), 200
    except Exception as e:
        return jsonify({"message": f"Error getting cam devices: {e}"}), 500


def getByUserId(user_id):
    try:
        cam_devices = manage_cam_device_model.ManageCamDevice.query.filter_by(
            user_id=user_id
        ).all()
        return jsonify([cam_device.serialize() for cam_device in cam_devices]), 200
    except Exception as e:
        return jsonify({"message": f"Error getting cam devices: {e}"}), 500


def delete(id):
    try:
        cam_device = manage_cam_device_model.ManageCamDevice.query.get(id)
        db.session.delete(cam_device)
        db.session.commit()
        return jsonify({"message": "Cam device deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"message": f"Error deleting cam device: {e}"}), 500


def update(data):
    try:
        cam_device = manage_cam_device_model.ManageCamDevice.query.get(data.get("id"))

        if not cam_device:
            return jsonify({"message": "Cam device not found!"}), 404

        # Verifica se algum campo válido foi enviado
        if not any(key in data for key in ["cam_name", "grupo"]):
            return jsonify({"message": "No valid data provided for update!"}), 400

        # Atualiza apenas os campos fornecidos na requisição
        if "cam_name" in data:
            cam_device.cam_name = data["cam_name"]
        if "grupo" in data:
            cam_device.grupo = data["grupo"]

        db.session.commit()
        return jsonify({"message": "Cam device updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating cam device: {str(e)}"}), 500
