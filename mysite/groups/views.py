from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Group
from .forms import GroupForm
from math import ceil
import json

class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    template_name = 'groups/create.html'
    success_url = '/'
    form_class = GroupForm

    def post(self, request, *args, **kwargs):
        form = GroupForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.admin = request.user
            f.save()

        return redirect(self.success_url)
    
class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Group
    template_name = 'groups/detail.html'

    def get(self, request, *args, **kwargs):
        if request.user == self.get_object().admin or self.get_object().members.contains(request.user):
            return super().get(request, *args, **kwargs)
        
        return HttpResponse("You are not allowed to view this group.", status=401)

class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    success_url = '/'

    def get(self, request, *args, **kwargs):
        group = self.get_object()
        if group.admin == request.user:
            group.delete()

        return redirect(self.success_url)
    
@login_required
def GroupInvitationView(request, pk):
    group = Group.objects.get(id=pk)

    if request.user in group.members.all() or request.user == group.admin:
        return redirect(reverse_lazy('groups:group', kwargs={'pk':pk}))

    if request.user.is_teacher():
        return render(request, 'groups/invitation_success.html', {'msg': "You can't join as you are a teacher."})

    if request.user in group.pending_requests.all():
        return redirect(reverse_lazy('groups:invitation_success'))
    
    if request.method == 'POST':
        group.pending_requests.add(request.user)
        return redirect(reverse_lazy('groups:invitation_success'))

    return render(request, 'groups/invitation.html', {'group': group})

def GroupInvitationSuccessView(request):
    return render(request, 'groups/invitation_success.html')

def get_pending_requests(request, group_id):
    group = Group.objects.get(pk=group_id)
    elements_in_page = 10

    if request.user == group.admin:
        page_num = int(request.GET.get('page', 1)) - 1
        data = [{'id': i.id, 'email': i.email, 'full_name': i.full_name, 'academic_id': i.academic_id}
                for i in group.pending_requests.all()[page_num*elements_in_page : min((page_num + 1)*elements_in_page, len(group.pending_requests.all()))]]
        return JsonResponse({'data':data, 'num_of_pages': ceil(len(group.pending_requests.all())/elements_in_page), 'current_page': page_num+1})
    
    return JsonResponse({'data': 'unauthorized'})

def get_students(request, group_id):
    group = Group.objects.get(pk=group_id)
    elements_in_page = 10

    if request.user == group.admin:
        page_num = int(request.GET.get('page', 1)) - 1
        data = [{'id': i.id, 'email': i.email, 'full_name': i.full_name, 'academic_id': i.academic_id}
                for i in group.members.all()[page_num*elements_in_page : min((page_num + 1)*elements_in_page, len(group.members.all()))]]
        return JsonResponse({'data':data, 'num_of_pages': ceil(len(group.members.all())/elements_in_page), 'current_page': page_num+1})
    
    return JsonResponse({'data': 'unauthorized'})

def remove_student(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode())

        group_id = json_data.get('group_id')
        student_id = json_data.get('student_id')

        group = Group.objects.get(pk=group_id)

        if request.user == group.admin:
            student = group.members.get(pk=student_id)
            group.members.remove(student)

            return JsonResponse({'id': student.id})

def reject_request(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode())

        group_id = json_data.get('group_id')
        student_id = json_data.get('student_id', None)

        group = Group.objects.get(pk=group_id)

        if request.user == group.admin:
            if json_data['all']:
                group.pending_requests.clear()
                return JsonResponse({})
            
            student = group.pending_requests.get(pk=student_id)
            group.pending_requests.remove(student)

            return JsonResponse({'id': student.id})

def accept_request(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode())

        group_id = json_data.get('group_id')
        student_id = json_data.get('student_id', None)

        group = Group.objects.get(pk=group_id)

        if request.user == group.admin:
            if json_data['all']:
                reqs = group.pending_requests
                group.members.add(*reqs.all())
                reqs.clear()

                return JsonResponse({})
            
            student = group.pending_requests.get(pk=student_id)
            group.pending_requests.remove(student)
            group.members.add(student)
            print(group.members.all())

            return JsonResponse({'id': student.id})