from django.contrib import admin
from .models import Post


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    pass
