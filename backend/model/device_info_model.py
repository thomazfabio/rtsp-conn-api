from database import db

class DeviceInfo(db.Model):
    __tablename__ = "device_info"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fabricante = db.Column(db.String(256), nullable=False)
    modelo = db.Column(db.String(256), nullable=False)
    path_rtsp = db.Column(db.String(256), nullable=False)
    versao = db.Column(db.String(100), nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "fabricante": self.fabricante,
            "modelo": self.modelo,
            "path_rtsp": self.path_rtsp,
            "versao": self.versao
        }
        
    def __repr__(self):
        return f"<DeviceInfo {self.id} - {self.fabricante} - {self.modelo}>"
