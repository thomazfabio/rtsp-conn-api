from database import db
from sqlalchemy.dialects.mysql import JSON

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.Enum("admin", "user"), default="user")
    user_status = db.Column(db.Enum("active", "inactive"), default="active")
    user_config = db.Column(JSON, nullable=True)

    def __repr__(self):
        return f"<User {self.username}>"