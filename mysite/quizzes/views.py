from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from .models import Quiz, Question, Choice, Grade
from groups.models import Group
from datetime import datetime, timedelta
from django.http import JsonResponse
import json


class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quizzes/detail.html'

    def post(self, request ,*args, **kwargs):
        quiz = self.get_object()

        total_questions = len(quiz.question_set.all())
        right_answers = 0
        for question in quiz.question_set.all():
            right_answer_id = question.choice_set.filter(is_correct=True).values_list('id', flat=True).first()
            selected_answer = request.POST.get(str(question.id))

            selected_answer_id = -1 if selected_answer is None else int(selected_answer)
            if right_answer_id == selected_answer_id:
                right_answers +=1

        grade = Grade(quiz=quiz, student=request.user, right_answers=right_answers, total_questions=total_questions)
        grade.save()

        group_id = quiz.group.id
        return HttpResponseRedirect(reverse_lazy('groups:group', kwargs={'pk':group_id }))
    
class QuizCreateView(CreateView):
    model = Quiz
    template_name = 'quizzes/create.html'
    fields = ["title", "start_time", "duration"]

    def dispatch(self, request, *args, **kwargs):
        self.group_id = kwargs['group_id']
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["group_id"] = self.group_id
        return context
    
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        duration = request.POST.get('duration')
        date = date.split('-')
        start_time = start_time.split(':')
        group_id = self.group_id
        group = Group.objects.get(pk=int(group_id))
        quiz = Quiz(title=title, 
                    start_time=datetime(year=int(date[0]), 
                                        month=int(date[1]), 
                                        day=int(date[2]), 
                                        hour=int(start_time[0]), 
                                        minute=int(start_time[1])), 
                    duration=timedelta(minutes=int(duration)),
                    group=group)
        quiz.save()
        return HttpResponseRedirect(reverse_lazy('groups:group', kwargs={'pk':group_id }))
    
def ShowQuestions(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    if request.method == 'GET':
        return render(request, 'quizzes/questions.html', {'quiz':quiz})
    
    data = json.loads(request.body.decode('utf-8'))
    question_text = data.get('question')
    choices = data.get('choices')
    question = Question(text=question_text, quiz=quiz)
    question.save()
    for choice in choices:
        c = Choice(text=choice['value'], is_correct=choice['checked'], question=question)
        c.save()
    return JsonResponse({'success': True})

class QuestionDeleteView(DeleteView):
    model = Question
    
    def get(self, request: HttpRequest, *args, **kwargs):
        question = self.get_object()
        quiz = question.quiz
        question.delete()
        return HttpResponseRedirect(reverse_lazy('quizzes:ShowQuestions', kwargs={'quiz_id':quiz.id}))