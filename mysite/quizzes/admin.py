from django.contrib import admin
from .models import Quiz, Choice, Question, Grade

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(Grade)