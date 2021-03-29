import jwt
from api.secret import jwt_key
from django.utils.datastructures import MultiValueDictKeyError
from django.core.cache import cache


def get_username_from_jwt(request):
    try:
        token = request.headers['Authorization'].split(' ')[1]
        try:
            username = jwt.decode(token, jwt_key, algorithms=[
                                  "HS256"])['username']
            return {'username': username}
        except (jwt.InvalidSignatureError, jwt.DecodeError) as e:
            return {'username': False, 'error_msg': 'Token is not valid'}

    except KeyError:
        return {'username': False, 'error_msg': 'Auth is required'}


def encode_username(username):
    return jwt.encode(
        {'username': username}, jwt_key, algorithm="HS256")


def get_pagination_props(request):
    try:
        page = int(request.GET['page'])
    except (MultiValueDictKeyError, ValueError) as e:
        page = 1

    try:
        per_page = int(request.GET['perPage'])
    except (MultiValueDictKeyError, ValueError) as e:
        per_page = 20

    return (page, per_page)


def objects_with_cache(key, cache_time, Model, pk=None):
    cache_values = cache.get(key)

    if cache_values is not None:
        return cache_values

    if pk is not None:
        objects = Model.objects.filter(pk=pk)
    else:
        objects = Model.objects.all()

    cache.set(key, objects, cache_time)
    return objects
