from django.contrib import admin
from .models import Login, Run, UserInfo

admin.site.register(Login)
admin.site.register(Run)
admin.site.register(UserInfo)