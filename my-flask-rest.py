# -*- coding: utf-8 -*-
from flask import Flask, g,request
from flask_restful import Api, Resource, reqparse, abort
from flask_httpauth import HTTPTokenAuth,HTTPBasicAuth,MultiAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json
app = Flask(__name__)
serializer = Serializer('hhhh', expires_in=1800)

api = Api(app)



users = [
    {'username': 'Tom', 'password': '111111'},
    {'username': 'Michael', 'password': '123456'}
]


token_auth = HTTPTokenAuth(scheme='Bearer')
basic_auth = HTTPBasicAuth()
# parser = reqparse.RequestParser()
# parser.add_argument('username', type=str)
# parser.add_argument('password', type=str)

@basic_auth.verify_password
def verify_password(Username,Password):

    g.user = None
    for user in users:
        if Username == user['username']:
            if Password == user['password']:
                g.user = Username

                return True
    return False


@token_auth.verify_token
def verify_token(token):


    user = serializer.loads(token)
    for myuser in users:
        if myuser['username'] == user:

            return True
    return False




class Login(Resource):

    decorators = [basic_auth.login_required]
    def get(self):
        token = serializer.dumps(g.user)
        print(g.user)
        return token.decode("utf-8"),200

class Index(Resource):
    decorators = [token_auth.login_required]
    def get(self):

        return "ok"



api.add_resource(Login,'/login')
api.add_resource(Index,'/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


