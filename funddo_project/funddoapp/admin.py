from django.contrib import admin

# Register your models here.
from models import UserProfile, Request

admin.site.register(Request)
admin.site.register(UserProfile)