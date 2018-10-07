from django.contrib import admin

# Register your models here.
from .models import Question, Solve, Tag

admin.site.register(Question)
admin.site.register(Solve)
admin.site.register(Tag)
