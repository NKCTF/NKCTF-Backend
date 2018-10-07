from django.contrib import admin

# Register your models here.
from .models import User, Team, Career

admin.site.register(User)
admin.site.register(Team)
admin.site.register(Career)
