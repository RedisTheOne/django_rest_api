from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from api.models import User, Post
from api.helpers import get_username_from_jwt, encode_username, parse_body_from_request
from api.serializers import Serializer, PostsSerializer
import json


@require_http_methods(['POST'])
def sign_up(request):
    data = parse_body_from_request(request)
    try:
        username = data['username']
        password = data['password']
        email = data['email']
        user = User.objects.get(username=username)
        return JsonResponse({'msg': f"User {username} already exists "}, status=400)
    except User.DoesNotExist:
        User(username=username, password=password, email=email).save()
        encoded_jwt = encode_username(username)
        return JsonResponse({'jwt': encoded_jwt}, status=201)
    except KeyError:
        return JsonResponse({'msg': 'Please fill required fields'}, status=400)


@require_http_methods(['POST'])
def sign_in(request):
    data = parse_body_from_request(request)
    try:
        user = User.objects.get(
            username=data['username'], password=data['password'])
        encoded_jwt = encode_username(data['username'])
        return JsonResponse({'jwt': encoded_jwt}, status=200)
    except KeyError:
        return JsonResponse({'msg': 'Please fill required fields'}, status=400)
    except User.DoesNotExist:
        return JsonResponse({'msg': 'User was not found'}, status=404)


@require_http_methods(['GET'])
def get_user_information(request):
    username_data = get_username_from_jwt(request)

    if username_data['username'] != False:
        try:
            user = User.objects.get(
                username=username_data['username'])
            posts = Post.objects.filter(user=user)
            posts_serializer = PostsSerializer(
                ['id', 'title', 'description', 'created_at'])
            posts_serialized = posts_serializer.getSerializedItems(posts)
            user_serializer = Serializer(
                ['id', 'username', 'email', 'password'])
            user_serialized = user_serializer.getSerializedItem(user)
            return JsonResponse({**user_serialized, ** {'posts': posts_serialized}})
        except User.DoesNotExist:
            return JsonResponse({'msg': 'User was not found'}, status=404)

    return JsonResponse({'msg': username_data['error_msg']}, status=401)
