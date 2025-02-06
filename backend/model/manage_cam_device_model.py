from database import db
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.sql import func  # Para usar funções SQL como CURRENT_TIMESTAMP

class ManageCamDevice(db.Model):
    __tablename__ = "manage_cam_devices"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID único para cada registro
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    device_id = db.Column(db.Integer, db.ForeignKey("device_info.id"), nullable=False, index=True)
    cam_name = db.Column(db.String(100), nullable=False)
    grupo = db.Column(db.String(50), nullable=True)
    full_cam_url_stream = db.Column(db.Text, nullable=True)
    full_cam_url_rtsp = db.Column(db.Text, nullable=True)
    cam_status = db.Column(db.Enum("online", "offline", "error"), default="offline")
    device_config = db.Column(JSON, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=func.now())  # Define a data de criação automaticamente
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())  # Atualiza sempre que o registro mudar

    def __repr__(self):
        return f"<ManageCamDevice {self.user_id} - {self.device_id}>"

