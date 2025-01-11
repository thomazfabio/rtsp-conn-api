from flask import Flask
from sqlalchemy import text  # Importa text para criar consultas SQL
from extensions.extensions import db
from routes.url_rtsp import url_rtsp
from routes.url_rtsp.models import UrlRtsp 

# create the Flask app

app = Flask(__name__)

# configure the MariaDb database
app.config["SQLALCHEMY_DATABASE_URI"] = "mariadb+mariadbconnector://fabio:root@127.0.0.1:3306/rtsp_conn_api"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def test_db_connection():
    try:
        with app.app_context():
            # Obtém uma conexão com o banco de dados
            with db.engine.connect() as connection:
                # Cria a consulta usando sqlalchemy.text
                result = connection.execute(text("SELECT 1"))
                for row in result:
                    print(f"Conexão bem-sucedida ao banco de dados! Resultado: {row[0]}")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return False
    return True

test_db_connection()

# Criação das tabelas (todas as tabelas definidas nos modelos)
with app.app_context():
    db.create_all()  # Cria as tabelas se não existirem

app.register_blueprint(url_rtsp, url_prefix='/url_rtsp')