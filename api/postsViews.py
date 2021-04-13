from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from api.models import Post, User
from api.serializers import PostSerializer, PostsSerializer
from api.helpers import get_username_from_jwt, get_pagination_props, objects_with_cache, posts_filtered_by_title_with_cache, parse_body_from_request
from django.utils import timezone
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.decorators import api_view

# class PostDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             return False

#     def get(self, request, id, format=None):
#         post = self.get_object(id)
#         if post == False:
#             return JsonResponse({'msg': 'Post was not found'}, status=404)
#         serializer = PostSerializer(post)
#         return JsonResponse(serializer.data)

#     def put(self, request, id, format=None):
#         post = self.get_object(id)
#         if post == False:
#             return JsonResponse({'msg': 'Post was not found'}, status=404)
#         request.data['created_at'] = post.created_at
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=204)
#         return JsonResponse(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         post = self.get_object(id)
#         if post == False:
#             return JsonResponse({'msg': 'Post was not found'}, status=404)
#         post.delete()
#         return JsonResponse({'msg': 'Post deleted successfully'}, status=204)


def getPost(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        post_serializer = PostsSerializer(
            ['id', 'title', 'description', 'created_at'])
        post_serialized = post_serializer.getSerializedItem(post)
        return JsonResponse(post_serialized)
    except Post.DoesNotExist:
        return JsonResponse({'msg': 'Post does not exist'}, status=404)


def getPosts(request):
    posts = objects_with_cache('posts', 10, Post)
    page, posts_per_page = get_pagination_props(request)
    p = Paginator(posts, posts_per_page)

    try:
        serializer = post_serializer = PostsSerializer(
            ['id', 'title', 'description', 'created_at'])
        post_serialized = post_serializer.getSerializedItems(
            p.page(page).object_list)
    except EmptyPage:
        return JsonResponse({'posts': [], 'page': page, 'postsPerPage': posts_per_page}, safe=False)

    return JsonResponse({'posts': post_serialized, 'page': page, 'postsPerPage': posts_per_page}, safe=False)


@api_view(['GET'])
def search_posts(request):
    try:
        query = request.GET['q']
    except MultiValueDictKeyError:
        return JsonResponse({'msg': 'q is required'}, status=400)

    posts = posts_filtered_by_title_with_cache(
        f"post-query-{query}", 10, Post, query)
    serializer = PostSerializer(posts, many=True)
    return JsonResponse(data=serializer.data, safe=False)
