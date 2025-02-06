from database import db

class DeviceInfo(db.Model):
    __tablename__ = "device_info"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fabricante = db.Column(db.String(256), nullable=False)
    modelo = db.Column(db.String(256), nullable=False)
    path = db.Column(db.String(256), nullable=False)
    versao = db.Column(db.String(100), nullable=False)