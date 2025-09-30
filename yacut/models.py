from sqlalchemy import func

from yacut import db
from yacut.constants import MAX_SHORT_LINK_ID_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, unique=True, nullable=False)
    short = db.Column(db.String(MAX_SHORT_LINK_ID_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=func.now())
