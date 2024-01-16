from django.contrib import admin
from .models import CustomUser

admin.site.site_header = 'QuizAT'
admin.site.site_title = 'QuizAT'

admin.site.register(CustomUser)
