from flask_restful import Resource, abort
from flask import jsonify
from data import db_session
from data.parser import user_parser
from data.users import User


class UsersResource(Resource):
    def get(self, id):
        db_secc = db_session.create_session()
        user = db_secc.query(User).get(id)
        if user:
            return jsonify({'user': user.to_dict()})
        return abort(404, message=f'User {id} not found')

    def delete(self, id):
        db_secc = db_session.create_session()
        user = db_secc.query(User).get(id)
        if user:
            db_secc.delete(user)
            db_secc.commit()
            return jsonify({'success': 'OK'})
        return abort(404, message=f'User {id} not found')


class UsersListResource(Resource):
    def get(self):
        db_secc = db_session.create_session()
        users = db_secc.query(User).all()
        return jsonify({'users': [i.to_dict() for i in users]})

    def post(self):
        args = user_parser.parse_args()
        db_secc = db_session.create_session()
        user = User(
            surname=args['surname'],
            age=args['age']
        )
        db_secc.add(user)
        db_secc.commit()
        return jsonify({'success': 'OK'})
