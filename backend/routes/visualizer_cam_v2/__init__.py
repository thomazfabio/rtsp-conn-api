from flask import Blueprint

visualizer_cam_v2 = Blueprint('visualizer_cam_v2', __name__)

from . import routes