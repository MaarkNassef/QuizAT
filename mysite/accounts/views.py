from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# TEMP
@login_required
def index(request):
    return render(request, 'base.html')