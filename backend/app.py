from flask import Flask
from add_url_rtsp import add_url_rtsp

app = Flask(__name__)

app.register_blueprint(add_url_rtsp, url_prefix='/add_url_rtsp')