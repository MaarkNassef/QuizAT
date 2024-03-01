from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from .models import Quiz, Question, Choice, Grade

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
            selected_answer_id = -1 if selected_answer is None else int(selected_answer[0])
            if right_answer_id == selected_answer_id:
                right_answers +=1

        grade = Grade(quiz=quiz, student=request.user, right_answers=right_answers, total_questions=total_questions)
        grade.save()

        group_id = quiz.group.id
        return HttpResponseRedirect(reverse_lazy('groups:group', kwargs={'pk':group_id }))