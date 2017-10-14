from flask import Flask, jsonify, make_response
from flask_restful import  Api, Resource, reqparse, fields, marshal
from flask_jwt import JWT, jwt_required, current_identity
from functools import wraps
import hashlib
from model import users
from pony.orm import *


db = Database()
db.bind(provider='mysql', host='78.155.199.27', user='zogdbadmin', passwd='p1l1d00b', db='zogdatabase')

class Dbusers(db.Entity):
    id = PrimaryKey(int, auto=True)
    login = Optional(str, unique=True)
    passhash = Optional(str)
    role = Optional(str, default='user')

sql_debug(False)
db.generate_mapping(create_tables=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'

api = Api(app, prefix="/api/v1")

class User(object):
    def __init__(self, id):
        self.id = id
        #https://github.com/vimalloc/flask-jwt-extended/issues/30
    def __str__(self):
        return "User(id='%s')" % self.id


def verify(username, password):
    if not (username and password):
        return False
    login=users.login(username,hashlib.md5(password.encode('utf-8')).hexdigest())
    if login:
        return User(id=login)


def identity(payload):
    user_id = payload['identity']
    if users.get(user_id):
        return {"id": user_id,
                "login": users.get(user_id)['login'],
                "role": users.get(user_id)['role']}
    else:
        return False


jwt = JWT(app, verify, identity)


def admin_required(f):
    @wraps(f)
    def new(*args, id=False):
        if not current_identity['role']=='admin':
            return make_response(jsonify({'error': 'Unauthorized access'}), 401)
        if id:
            return f(*args, id)
        else:
            return f(*args)
    return new


class UsersAPI(Resource):
    def __init__(self):
        self.argparser = reqparse.RequestParser()
        self.argparser.add_argument('login')
        self.argparser.add_argument('password')
        super(UsersAPI, self).__init__()

    @jwt_required()
    @admin_required
    def get(self):
        userslist=users.get()
        return jsonify({"users":userslist})

    @jwt_required()
    def post(self):
        args = self.argparser.parse_args()
        return users.post(
            {
            'login': args['login'],
            'password': args['password']
            })

class UserAPI(Resource):
    @jwt_required()
    def get(self, id):
        if id=='current':
            id=current_identity['id']
        if not current_identity['role']=='admin' and not id==current_identity['id']:
            return make_response(jsonify({'error': 'Unauthorized access'}), 401)
        result=users.get(id)
        if result:
            return jsonify(result)
        else:
            return make_response(jsonify({'error': 'User not found'}), 404)
        pass

    @jwt_required()
    def patch(self, id):
        pass

    @jwt_required()
    @admin_required
    def delete(self, id):
        if id=='current'or id==current_identity['id']:
            return make_response(jsonify({'error': 'You cannot delete yourself'}), 400)
        if not current_identity['role']=='admin' and not id==current_identity['id']:
            return make_response(jsonify({'error': 'Unauthorized access'}), 401)
        if not users.get(id):
            return make_response(jsonify({'error': 'User not found'}), 404)
        if users.delete(id):
            return '', 204
        else:
            return make_response(jsonify({'error': 'Something wrong'}), 500)


api.add_resource(UsersAPI, '/users', endpoint='users')
api.add_resource(UserAPI, '/users/<id>', endpoint='user')

if __name__ == '__main__':
    app.run(debug=True)