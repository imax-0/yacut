import re

from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import URLField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from yacut.constants import (
    MAX_SHORT_LINK_ID_LENGTH,
    FORBIDDEN_SHORT_LINKS
)


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(
                max=MAX_SHORT_LINK_ID_LENGTH,
                message=f'Короткая сссылка не должна быть длинее {MAX_SHORT_LINK_ID_LENGTH} символов.'
            )
        ]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        short_id = field.data

        if not short_id:
            return

        if not re.match(r'^[a-zA-Z0-9]+$', short_id):
            raise ValidationError('Можно использовать только латинсике буквы и цифры.')
 
        if short_id.lower() in FORBIDDEN_SHORT_LINKS:
            raise ValidationError('Предложенный вариант короткой ссылки уже существует.')


class DownloadToDiskForm(FlaskForm):
    files = MultipleFileField()
    submit = SubmitField('Загрузить')
