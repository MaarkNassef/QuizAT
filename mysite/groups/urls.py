from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('add/', views.GroupCreateView.as_view(), name="add_group"),
]
