from flask import Blueprint

add_url_rtsp = Blueprint('add_url_rtsp', __name__)

from . import routes