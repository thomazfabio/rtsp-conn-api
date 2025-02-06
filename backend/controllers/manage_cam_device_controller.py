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
            device_config=data.get("device_config")
        )
        db.session.add(new_cam_device)
        db.session.commit()
        return jsonify({"message": "Cam device created successfully!"}), 201
    except Exception as e:
        return jsonify({"message": f"Error creating cam device: {e}"}), 500
    