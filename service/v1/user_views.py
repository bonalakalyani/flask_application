import datetime
import os
import logging

import jwt
from dotenv import load_dotenv
from flask import request, abort, jsonify, current_app as app
from flask_restx import Api, Resource, Namespace, fields
from werkzeug.security import generate_password_hash

from service.models import db, UserSchema, User, BlacklistedToken
from service.decorators import token_required
from service.custom_exceptions import CustomException
from service.custom_log import *


load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
REFRESH_SECRET_KEY = os.environ.get('REFRESH_SECRET_KEY')
TOKEN_EXPIRATION_TIME = datetime.timedelta(minutes=30)
REFRESH_TOKEN_EXPIRATION_TIME = datetime.timedelta(days=1)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(filename)s:%(lineno)d ''%(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)



api = Namespace('users', description='User related information')

parser = api.parser()
parser.add_argument('x-access-tokens', location='headers')
parser.add_argument('x-refresh-tokens', location='headers')

create_user_fields = api.model('createuser', {
    'email': fields.String,
    'password': fields.String
})


class CreateUser(Resource):
    user_schema = UserSchema()

    @api.doc('create user')
    @api.doc(body=create_user_fields, parser=parser)
    def post(self):
        ''' create user '''
        payload = request.json
        errors = self.user_schema.validate(payload)
        if errors:
            abort(400, str(errors))

        if User.query.filter_by(email=payload['email']).first():
            return jsonify({'message': 'User email already registered'})
        hashed_password = generate_password_hash(payload['password'], method='sha256')
        new_user = User(email=payload['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        logger.info('User authentication successful %s', new_user)
        return jsonify({'message': 'registered successfully'})


api.add_resource(CreateUser, '/v1/user/createuser')


class UserAuthToken(Resource):
    user_schema = UserSchema()

    @api.doc('user authorization token')
    def post(self):
        ''' authorization token for user'''
        try:
            if not request.args:
                abort(400, "Invalid parameters")
            email = request.args.get('email')
            password = request.args.get('password')
            user = User.query.filter_by(email=email).first()

            if not user:
                response = jsonify({'message': 'Invalid Credential'})
                response.status_code = 400
                return response

            if user.is_correct_password(password):
                token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() +
                                    TOKEN_EXPIRATION_TIME},
                                    SECRET_KEY)
                refresh_token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() +
                                            REFRESH_TOKEN_EXPIRATION_TIME},
                                            REFRESH_SECRET_KEY)

                logger.info('User authentication successful')
                return jsonify({'token': token.decode('UTF-8'), 'refresh': refresh_token.decode('UTF-8')})
            else:
                response = jsonify({'message': 'Invalid Credential'})
                response.status_code = 400
                return response
        except Exception as e:
            logger.exception('Error occurred while generating user authorization token')
            abort(500, "Internal server error")



api.add_resource(UserAuthToken, '/v1/user/authtoken')


class RefreshToken(Resource):
    @api.doc('refresh authorization token')
    def post(self):
        ''' refresh authorization token '''
    
        if 'x-refresh-tokens' not in request.headers:
            abort(400, "Missing refresh token")

        refresh_token = request.headers['x-refresh-tokens']
        try:
            refresh_data = jwt.decode(refresh_token, REFRESH_SECRET_KEY)
            user = User.query.filter_by(id=refresh_data['user_id']).first()
        except jwt.InvalidTokenError:
            abort(401, "Invalid refresh token")

        token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() +
                            TOKEN_EXPIRATION_TIME},
                            SECRET_KEY)

        logger.info('Token refreshed successfully')
        return jsonify({'token': token.decode('UTF-8')})


api.add_resource(RefreshToken, '/v1/user/refresh-token')



class UserLogout(Resource):
    method_decorators = [token_required]

    def post(self, user):
        ''' logout user and blacklist token '''
        
        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]
            if token:
                blacklisted_token = BlacklistedToken(token=token)
                db.session.add(blacklisted_token)
                db.session.commit()

                logger.info('User logged out successfully')
                return jsonify({'message': 'User logged out successfully'})
        abort(400, 'Invalid token')
        

api.add_resource(UserLogout, '/v1/user/logout')


class UserDetails(Resource):
    method_decorators = [token_required]

    @api.doc('user detail')
    def get(self, user):
        ''' details of user'''
        try:
            u_info = dict()
            u_info["user_id"] = user.id
            u_info["email"] = user.email

            logger.info('User details retrieved successfully')
            return jsonify(u_info)
        except Exception as e:
            logger.exception('Error occurred while retrieving user details')
            abort(500, "Internal server error")

api.add_resource(UserDetails, '/v1/user/userdetails')
