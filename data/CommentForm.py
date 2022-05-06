from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    comments = TextAreaField("Ваш комментарии:", validators=[DataRequired()])
    stars = IntegerField('Ваша оценка игры?', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
