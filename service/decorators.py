import jwt
import os
from functools import wraps
from .models import User, BlacklistedToken
from flask import jsonify, request


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        access_token = None

        if 'x-access-tokens' in request.headers:
            access_token = request.headers['x-access-tokens']

        if not access_token:
            return jsonify({'message': 'Access token is missing'})

        blacklisted_token = BlacklistedToken.query.filter_by(token=access_token).first()
        if blacklisted_token:
            return jsonify({'message': 'Invalid access token'})

        try:
            access_data = jwt.decode(access_token, os.environ['SECRET_KEY'])
            current_user = User.query.filter_by(id=access_data['user_id']).first()
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid access token'})

        return f(current_user, *args, **kwargs)

    return decorator


