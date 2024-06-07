from django.contrib import admin
from .models import ZerowaveUser
# Register your models here.
class Useradmin(admin.ModelAdmin):
    list_display = ('nickname', 'email', 'password')

admin.site.register(ZerowaveUser, Useradmin)