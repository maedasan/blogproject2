from django.contrib import admin
from .models import BlogModel, Comment


admin.site.register(BlogModel)
admin.site.register(Comment)
