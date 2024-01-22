from typing import Any
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from .models import Group
from .forms import GroupForm

class GroupCreateView(CreateView):
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
    
class GroupDetailView(DetailView):
    model = Group
    template_name = 'groups/detail.html'