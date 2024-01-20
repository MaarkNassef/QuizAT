from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from groups.models import Group

@login_required
def index(request):
    return render(request, 'main/index.html' , {'group_list': Group.objects.all()})