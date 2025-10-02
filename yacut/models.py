import re

from sqlalchemy import func
from sqlalchemy.orm import validates

from yacut import db
from yacut.constants import MAX_SHORT_LINK_ID_LENGTH, FORBIDDEN_SHORT_LINKS


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(MAX_SHORT_LINK_ID_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=func.now())


    @validates('short')
    def validate_short(self, key, short_id):
        if not short_id:
            raise ValueError("Короткая ссылка не может быть пустой")

        if not re.match(r'^[a-zA-Z0-9]+$', short_id):
            raise ValueError("Короткая ссылка может содержать только латинские буквы и цифры")

        if short_id.lower() in FORBIDDEN_SHORT_LINKS:
            raise ValueError('Предложенный вариант короткой ссылки уже существует.')

        return short_id
