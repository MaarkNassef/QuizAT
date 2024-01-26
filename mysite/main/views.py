from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from groups.models import Group

@login_required
def index(request):
    groups = None
    if request.user.is_teacher():
        groups = Group.objects.filter(admin=request.user)
    else:
        groups = [i for i in Group.objects.all() if i.members.contains(request.user)]

    return render(request, 'main/index.html' , {'group_list': groups})