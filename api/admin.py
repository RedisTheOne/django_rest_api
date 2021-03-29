from django.contrib import admin
from .models import Post, Comment

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Content information', {'fields': ['title', 'description']}),
        ('Date information', {'fields': ['created_at']})
    ]


class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Post information', {'fields': ['post']}),
        ('Content information', {'fields': ['text']})
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
