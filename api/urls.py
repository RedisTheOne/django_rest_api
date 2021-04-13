from django.urls import path
from . import userViews, postsViews, commentsViews

urlpatterns = [
    path('user/signup/', userViews.sign_up, name='sign_up'),
    path('user/signin/', userViews.sign_in, name='sign_in'),
    path('user/', userViews.get_user_information, name='get_user_information'),
    path('posts/', postsViews.getPosts, name='get_posts'),
    path('posts/<int:post_id>/', postsViews.getPost, name='get_post'),
    path('posts/search/', postsViews.search_posts, name='search_posts'),
    path('posts/<int:post_id>/comments/', commentsViews.Comments.as_view())
]
