from django.contrib import admin

# Register your models here.
from .models import Mail, JoinRequest

admin.site.register(Mail)
admin.site.register(JoinRequest)