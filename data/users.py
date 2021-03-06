import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin  # мб можно убрать
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, SerializerMixin, UserMixin):
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    pony_run_install = sqlalchemy.Column(sqlalchemy.Integer,
                                         nullable=True, default=0)
    politopy_install = sqlalchemy.Column(sqlalchemy.Integer,
                                         nullable=True, default=0)
    comments_politopy = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    comments_pony_run = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    stars_politopy = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    stars_pony_run = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
