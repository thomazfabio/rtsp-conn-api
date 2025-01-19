from flask import Blueprint

visualizer_cam = Blueprint('visualizer_cam', __name__)

from . import routes