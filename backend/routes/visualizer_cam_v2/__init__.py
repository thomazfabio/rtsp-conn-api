from flask import Blueprint

visualizer_cam_v2 = Blueprint('visualizer_cam_v2', __name__)
stream_manager =  Blueprint('stream_manager', __name__)

from . import routes