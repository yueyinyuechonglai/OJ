from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Problem, MyUser
from .forms import UserForm
# Create your views here.

def problem_list(request,page):
    PAGENUM = 1
    start = (page-1) * PAGENUM
    stop = page * PAGENUM

    myslice = slice(start,stop,1)
    problems = Problem.objects.order_by('prob_id')
    npage = (len(problems)-1) // PAGENUM + 1
    pages = []
    for i in range(1,npage+1):
        pages.append(i)

    problems = problems[myslice]

    return render(request, 'problem_list.html', {'problems': problems,'page' : page,'pages' : pages})

def prob_detail(request,prob_id):
    problem = Problem.objects.get(prob_id = prob_id)
    return render(request, 'prob_detail.html', {'problem': problem})

def submit(request,prob_id):
    #判断是否登录,若登录则跳到submit页面,否则登录页面
    return render(request,'submit.html',{'prob_id': prob_id})

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

def sign_in(request):
    def form_vaild():
        user = authenticate(\
            username=form.cleaned_data["username"],\
            password=form.cleaned_data["password"])
        isUserExist = False
        if user is not None:
            if user.is_active:
                login(request, user)
            isUserExist = True
        if isUserExist:
            return problem_list(request, 1)
        else:
            error = {"msg": "The name or password is incorrect."}
            return render(request, 'sign_in.html', error)

    def form_not_vaild():
        inputedData = {}
        inputedData["name"] = request.POST.get("name", "")
        inputedData["password"] = request.POST.get("password", "")
        return render(request, 'memories/sign_in.html', {'input': inputedData})
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            return form_vaild()
        else:
            return form_not_vaild()
    else:
        backToLogin = True
        if request.user.is_authenticated:
            if request.GET.get("_logout", "") == "log out":
                logout(request)
            else:
                backToLogin = False
        if backToLogin:
            return render(request, 'sign_in.html')
        else:
            return problem_list(request, 1)
