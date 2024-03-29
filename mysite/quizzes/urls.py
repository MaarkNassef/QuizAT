from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('<int:pk>/', views.QuizDetailView.as_view(), name='QuizDetailView'),
    path('create/<int:group_id>/', views.QuizCreateView.as_view(), name='QuizCreateView'),
    path('questions/<int:quiz_id>/', views.ShowQuestions, name='ShowQuestions'),
    path('grades/<int:quiz_id>/', views.ShowGrades, name='ShowGrades'),
    path('download_grades/<int:quiz_id>/', views.DownloadGrades, name='DownloadGrades'),
    path('questions/delete/<int:pk>/', views.QuestionDeleteView.as_view(), name='QuestionDeleteView'),
]