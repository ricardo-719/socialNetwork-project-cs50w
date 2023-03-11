from django.contrib import admin
from .models import User, Post, Profile, Follows, Likes

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Follows)
admin.site.register(Likes)