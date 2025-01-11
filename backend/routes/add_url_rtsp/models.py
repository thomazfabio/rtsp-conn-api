from  extensions.extensions import db

class UrlRtsp(db.Model):
    __tablename__ = 'url_rtsp'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    url = db.Column(db.String(200))
    group = db.Column(db.String(100))
    channel = db.Column(db.String(100))
    name = db.Column(db.String(100))