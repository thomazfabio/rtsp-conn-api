from flask import Flask
from sqlalchemy import text  # Importa text para criar consultas SQL
from database import db
from routes import (
    manage_cam_device_route,
    device_info_route,
    stream_route,
    services_route,
)
from flask_cors import CORS
from model import device_info_model, users_model
from flask_restx import Api

# importando Namespaces
from routes.services_route import ns as services_ns


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
                    print(
                        f"Conexão bem-sucedida ao banco de dados! Resultado: {row[0]}"
                    )
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return False
    return True


test_db_connection()

# Criação das tabelas no banco de dados
with app.app_context():
    db.create_all()

# Registra os Blueprints
# app.register_blueprint(services_route.url_rtsp_bp, url_prefix="/services")
app.register_blueprint(
    manage_cam_device_route.manage_cam_device_bp, url_prefix="/manage_cam_device"
)
# app.register_blueprint(device_info_route.device_info_bp, url_prefix="/device_info")
app.register_blueprint(stream_route.stream, url_prefix="/stream")

api = Api(
    app,
    version="1.0.0",
    title="API Video Streaming | Frame Processing | RTSP Management",
    description="API para gerenciamento de câmeras RTSP, Streaming de video e tratamento de FRAMES.",
    contact="Fabio Thomaz da Silva",
    contact_email="fabio_thomaz@live.com",
    license="MIT",
    license_url="https://opensource.org/licenses/MIT",
    doc="/docs",  # altera o endpoint da documentação (padrão é /)
)

api.add_namespace(services_ns, path="/services")
api.add_namespace(device_info_route.ns, path="/device_info")  # Adiciona o namespace de device_info
