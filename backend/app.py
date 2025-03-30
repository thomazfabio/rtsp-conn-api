
from flask import Flask
from sqlalchemy import text  # Importa text para criar consultas SQL
from database import db
from routes.url_rtsp import url_rtsp
from routes.visualizer_cam import visualizer_cam
from routes.visualizer_cam_v2 import visualizer_cam_v2
from routes import manage_cam_device_route, device_info_route
from flask_cors import CORS
from model import device_info_model, users_model
from routes.url_rtsp.models import UrlRtsp

# Criação do Flask app
app = Flask(__name__)

# Configura CORS para permitir conexões WebSocket
CORS(app)



# Configuração do banco de dados MariaDB
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mariadb+mariadbconnector://fabio:root@127.0.0.1:3306/rtsp_conn_api"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Testa a conexão com o banco de dados
def test_db_connection():
    try:
        with app.app_context():
            with db.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                for row in result:
                    print(f"Conexão bem-sucedida ao banco de dados! Resultado: {row[0]}")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return False
    return True

test_db_connection()

# Criação das tabelas no banco de dados
with app.app_context():
    db.create_all()

# Registra os Blueprints
app.register_blueprint(url_rtsp, url_prefix="/url_rtsp")
app.register_blueprint(visualizer_cam, url_prefix="/visualizer_cam")
app.register_blueprint(visualizer_cam_v2, url_prefix="/visualizer_cam_v2")
app.register_blueprint(manage_cam_device_route.manage_cam_device_bp, url_prefix="/manage_cam_device")
app.register_blueprint(device_info_route.device_info_bp, url_prefix="/device_info")


