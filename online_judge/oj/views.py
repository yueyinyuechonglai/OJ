from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    return render(request, 'index.html')

def sign_up(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                error = {'msg': "The username has already existed."}
                return render(request, 'sign_up.html', error)
            else:
                user = MyUser.objects.create_user(\
                    username = form.cleaned_data['username'],\
                    email = form.cleaned_data['email'],\
                    password = form.cleaned_data['password'],)
                user.save()
    return render(request, 'sign_up.html')

def login(request):
    pass
