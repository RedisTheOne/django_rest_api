from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from api.models import Comment, Post
from api.serializers import CommentSerializer
from api.helpers import get_username_from_jwt, get_pagination_props, objects_with_cache
from django.core.paginator import Paginator, EmptyPage


class Comments(APIView):
    def get(self, request, post_id, format=None):
        comments = objects_with_cache(
            f"comments-with-post-id-{post_id}", 10, Comment, post_id)
        page, comments_per_page = get_pagination_props(request)
        p = Paginator(comments, comments_per_page)

        try:
            serializer = CommentSerializer(p.page(page).object_list, many=True)
        except EmptyPage:
            return JsonResponse({'posts': [], 'page': page, 'commentsPerPage': comments_per_page}, safe=False)

        return JsonResponse({'comments': serializer.data, 'page': page, 'commentsPerPage': comments_per_page}, safe=False)

    def post(self, request, post_id, format=None):
        username_data = get_username_from_jwt(request)

        if username_data['username'] != False:
            data = JSONParser().parse(request)
            serializer = CommentSerializer(data=data)

            if serializer.is_valid():
                try:
                    post = Post.objects.get(pk=post_id)
                except Post.DoesNotExist:
                    return JsonResponse({'msg': 'Post was not found'}, status=404)

                comment = Comment(text=serializer.data['text'],
                                  post=post)
                comment.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

        return JsonResponse({'msg': username_data['error_msg']}, status=400)
