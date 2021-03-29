import jwt
from api.secret import jwt_key


def get_username_from_jwt(request):
    try:
        token = request.headers['Authorization'].split(' ')[1]
        try:
            username = jwt.decode(token, jwt_key, algorithms=[
                                  "HS256"])['username']
            return {'username': username}
        except jwt.InvalidSignatureError:
            return {'username': False, 'error_msg': 'Token is not valid'}
        except jwt.DecodeError:
            return {'username': False, 'error_msg': 'Token is not valid'}
    except KeyError:
        return {'username': False, 'error_msg': 'Auth is required'}


def encode_username(username):
    return jwt.encode(
        {'username': username}, jwt_key, algorithm="HS256")
