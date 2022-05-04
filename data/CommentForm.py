from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    comments = TextAreaField("Ваши комментарии:", validators=[DataRequired()])
    submit = SubmitField('Сохранить')
