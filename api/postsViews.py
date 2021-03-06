from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from api.models import Post, User
from api.serializers import PostSerializer
from api.helpers import get_username_from_jwt, get_pagination_props, objects_with_cache, posts_filtered_by_title_with_cache
from django.utils import timezone
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.decorators import api_view


class Posts(APIView):
    def get(self, request, format=None):
        posts = objects_with_cache('posts', 10, Post)
        page, posts_per_page = get_pagination_props(request)
        p = Paginator(posts, posts_per_page)

        try:
            serializer = PostSerializer(p.page(page).object_list, many=True)
        except EmptyPage:
            return JsonResponse({'posts': [], 'page': page, 'postsPerPage': posts_per_page}, safe=False)

        return JsonResponse({'posts': serializer.data, 'page': page, 'postsPerPage': posts_per_page}, safe=False)

    def post(self, request, format=None):
        # Check if user is authed or not
        username_data = get_username_from_jwt(request)
        if username_data['username'] != False:
            # Parse and create post
            data = JSONParser().parse(request)
            data['created_at'] = created_at = timezone.now()
            serializer = PostSerializer(data=data)

            if serializer.is_valid():
                user = User.objects.get(username=username_data['username'])
                post = Post(title=serializer.data['title'],
                            description=serializer.data['description'],
                            user=user,
                            created_at=serializer.data['created_at'])
                post.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse({'msg': username_data['error_msg']}, status=400)


class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return False

    def get(self, request, id, format=None):
        post = self.get_object(id)
        if post == False:
            return JsonResponse({'msg': 'Post was not found'}, status=404)
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)

    def put(self, request, id, format=None):
        post = self.get_object(id)
        if post == False:
            return JsonResponse({'msg': 'Post was not found'}, status=404)
        request.data['created_at'] = post.created_at
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=204)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        post = self.get_object(id)
        if post == False:
            return JsonResponse({'msg': 'Post was not found'}, status=404)
        post.delete()
        return JsonResponse({'msg': 'Post deleted successfully'}, status=204)


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
