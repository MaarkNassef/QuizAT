from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
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
    
@login_required
def GroupInvitationView(request, pk):
    group = Group.objects.get(id=pk)

    if request.user in group.pending_requests.all():
        return redirect(reverse_lazy('groups:invitation_success'))
    
    if request.user in group.members.all():
        return redirect(reverse_lazy('groups:group', kwargs={'pk':pk}))

    if request.method == 'POST':
        group.pending_requests.add(request.user)
        return redirect(reverse_lazy('groups:invitation_success'))

    return render(request, 'groups/invitation.html', {'group': group})

def GroupInvitationSuccessView(request):
    return render(request, 'groups/invitation_success.html')