from flask import Blueprint

url_rtsp = Blueprint('url_rtsp', __name__)

from . import routes