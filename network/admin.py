from django.contrib import admin
from .models import User, Post
# Register your models here.

class FollowAdmin(admin.ModelAdmin):
    filter_horizontal = ("following", "followers",)

class LikeAdmin(admin.ModelAdmin):
    filter_horizontal = ("like",)


admin.site.register(User, FollowAdmin)
admin.site.register(Post, LikeAdmin)
