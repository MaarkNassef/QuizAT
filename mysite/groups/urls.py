from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('add/', views.GroupCreateView.as_view(), name="add_group"),
    path('<int:pk>/', views.GroupDetailView.as_view(), name="group"),
    path('<int:pk>/delete/', views.GroupDeleteView.as_view(), name="delete_group"),
    path('invitation/<int:pk>', views.GroupInvitationView, name="invitation"),
    path('invitation_success', views.GroupInvitationSuccessView, name="invitation_success")
]
