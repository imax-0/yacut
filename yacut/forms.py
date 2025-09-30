from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import URLField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from yacut.constants import MIN_SHORT_LINK_ID_LENGTH, MAX_SHORT_LINK_ID_LENGTH


class URLMapForm(FlaskForm):
    original_link = URLField(
        "Длинная ссылка",
        validators=[DataRequired(message="Обязательное поле")]
    )
    custom_id = StringField(
        "Ваш вариант короткой ссылки",
        validators=[Length(min=MIN_SHORT_LINK_ID_LENGTH, max=MAX_SHORT_LINK_ID_LENGTH)]
    )
    submit = SubmitField('Создать')


class DownloadToDiskForm(FlaskForm):
    files = MultipleFileField()
    submit = SubmitField('Загрузить')
