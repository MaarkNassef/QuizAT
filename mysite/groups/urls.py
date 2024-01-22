from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('add/', views.GroupCreateView.as_view(), name="add_group"),
    path('<int:pk>/', views.GroupDetailView.as_view(), name="group"),
]
