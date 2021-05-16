from enum import unique
import uuid
from datetime import datetime

from api_v1 import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON, UUID

db = SQLAlchemy(app)

class ImageApiRequest(db.Model):
    __tablename__ = "image_api_request"

    id =db.Column(db.Integer, primary_key=True)
    request_id = db.Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    images = db.Column(JSON, server_default='{}')
    image_src = db.relationship('ImageList', backref='image_api', lazy=True)
    is_completed = db.Column(db.Boolean, server_default=u'false', nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class ImageList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_request_id = db.Column(db.Integer, db.ForeignKey('image_api_request.id'))
    





