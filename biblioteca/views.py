from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required(login_url='/account/login/')
def home(request):
    return render(request, 'biblioteca/home.html')