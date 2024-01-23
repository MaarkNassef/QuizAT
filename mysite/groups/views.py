from django.shortcuts import redirect
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Group
from .forms import GroupForm

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

class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    success_url = '/'

    def get(self, request, *args, **kwargs):
        group = self.get_object()
        if group.admin == request.user:
            group.delete()
            
        return redirect(self.success_url)