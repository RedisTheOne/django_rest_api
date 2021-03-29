from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from api.serializers import UserSerializer, FilteredUserSerializer, UserSignInSerializer
from api.models import User
from api.helpers import get_username_from_jwt, encode_username


@api_view(['POST'])
def sign_up(request):
    data = JSONParser().parse(request)
    serializer = UserSerializer(data=data)

    if serializer.is_valid():
        username = data['username']
        try:
            user = User.objects.get(username=username)
            return JsonResponse({'msg': f"User {username} already exists "}, status=400)
        except User.DoesNotExist:
            serializer.save()
            encoded_jwt = encode_username(username)
            return JsonResponse({'jwt': encoded_jwt}, status=201)

    return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
def sign_in(request):
    data = JSONParser().parse(request)
    serializer = UserSignInSerializer(data=data)

    if serializer.is_valid():
        username = data['username']
        password = data['password']
        try:
            User.objects.get(username=username, password=password)
            encoded_jwt = encode_username(username)
            return JsonResponse({'jwt': encoded_jwt}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'msg': 'User was not found'}, status=404)

    return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
def get_user_information(request):
    username_data = get_username_from_jwt(request)

    if username_data['username'] != False:
        try:
            user = User.objects.get(
                username=username_data['username'])
            serializer = FilteredUserSerializer(user)
            return JsonResponse(serializer.data)
        except User.DoesNotExist:
            return JsonResponse({'msg': 'User was not found'}, status=404)

    return JsonResponse({'msg': username_data['error_msg']}, status=401)
