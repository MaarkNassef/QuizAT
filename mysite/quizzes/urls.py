from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('<int:pk>/', views.QuizDetailView.as_view(), name='QuizDetailView'),
]