from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import CustomUserCreationForm

# TEMP
@login_required
def index(request):
    return render(request, 'base.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse_lazy('index'))
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})
