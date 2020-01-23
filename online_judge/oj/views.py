import os
import time
import _thread
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.db.models import Sum, Count
# Create your views here.

def problem_list(request, page):
    PAGENUM = 1
    start = (page-1) * PAGENUM
    stop = page * PAGENUM

    pro_count = Problem.objects.count()

    if stop > pro_count:
        stop = pro_count
    myslice = slice(start,stop,1)
    problems = Problem.objects.order_by('prob_id')
    last_page = (pro_count-1) // PAGENUM + 1
    pages = []
    for i in range(1,last_page+1):
        pages.append(i)

    problems = problems[myslice]

    return render(request, 'problem_list.html', {'problems': problems,'page' : page,'pages' : pages})

def prob_detail(request, prob_id):
    problem = Problem.objects.get(prob_id = prob_id)
    return render(request, 'prob_detail.html', {'problem': problem})

def submit(request, prob_id):
    #判断是否登录,若登录则跳到status页面,否则登录页面

    def download_file(myFile):
        if not myFile:
            return HttpResponse("no files for upload!")
        Submission.submit_count += 1
        myFile.name = str(Submission.submit_count)
        if form.cleaned_data['lang'] == 'C':
            myFile.name += '.c'
        elif form.cleaned_data['lang'] == 'C++':
            myFile.name += '.cpp'

        file_path = os.path.join(".", "oj", "submitted_code", myFile.name)

        destination = open(file_path, 'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()

    def compile_code(form, file_path):
        submit_status = ""
        if form.cleaned_data['lang'] == 'C':
            os.system("gcc -o2 " + file_path + " 2> compile_info")
            compile_info = open('compile_info', 'r').read()

            if "error" in compile_info:
                submit_status = 'Compile Error'
            else:
                os.system("gcc " + file_path + " -o2  -o now_exe")
        elif form.cleaned_data['lang'] == 'C++':
            os.system("g++ " + file_path + " -o2 -std=c++11 " + "2> compile_info")
            compile_info = open('compile_info', 'r').read()

            if "error" in compile_info:
                submit_status = 'Compile Error'
            else:
                os.system("g++ " + file_path + " -o2 -std=c++11 "+ "-o now_exe")
        return submit_status

    if request.method == "POST":
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user.is_authenticated:
                # check, compile and run code and compare the answer and output
                myFile = request.FILES.get("code", None)
                download_file(myFile)

                file_path = os.path.join(".", "oj", "submitted_code", myFile.name)

                submit_status = compile_code(form, file_path)

                if submit_status != 'Compile Error':

                    def run_code():
                        data_path = os.path.join(".", "oj", "static", "problem_data", str(prob_id),"1.in")
                        os.system("now_exe"+" < "+data_path+" > 1.ans")

                    def count_time():
                        start_time = time.time()
                        while time.time() - start_time < 1.0:
                            pass
                        now_path=os.path.join('now_exe.exe')
                        os.system("taskkill /f /t /im " + now_path + " 2> information")

                    def make_file(name):
                        f = open(name, "w")
                        f.close()

                    make_file('information')
                    try:
                        _thread.start_new_thread( run_code, () )
                        _thread.start_new_thread( count_time, () )
                    except:
                        print ("Error")

                    time.sleep(2)
                    information = open("information","r").read()
                    # print(information)
                    if ("now_exe.exe" not in information):
                        submit_status = 'tle'
                    else:
                        data_path = os.path.join(".", "oj", "static", "problem_data",str(prob_id),"1.out")
                        make_file('result')
                        os.system("fc 1.ans "+data_path + "> result")
                        result = open('result','r').read()
                        # print(result)
                        if ("FC: " in result):
                            submit_status = 'Accepted'
                        else:
                            submit_status = 'Wrong Answer'
                print(submit_status)
                # print(models.Problem.objects.filter(prob_id=prob_id))
                os.system("del now_exe.exe")
                os.system("del 1.ans")
                os.system("del result")
                os.system("del information")
                os.system("del compile_info")
                os.system("del 2.exe")

                submission = Submission.objects.create(
                    subm_id = Submission.objects.count(),
                    prob_id = prob_id,
                    value = myFile.read(),
                    user = request.user.username,
                    exe_time = 0,
                    status = submit_status,
                    language = form.cleaned_data['lang'],
                )
                return status(request,1)
            else:
                return sign_in(request, True)
        else:
            print(form.cleaned_data)
            print(form.errors)
            return render(request, '404.html')
    else:
        return render(request, '404.html')

def status(request,page):
    PAGENUM = 3
    start = (page-1) * PAGENUM
    stop = page * PAGENUM

    sub_count = Submission.objects.count()
    last_page = (sub_count-1) // PAGENUM + 1

    if stop > sub_count:
        stop = sub_count

    myslice = slice(start,stop,1)
    submissions = Submission.objects.order_by('-subm_id')

    submissions = submissions[myslice]

    return render(request,'status.html',{'submissions': submissions,'page' : page,'last_page' : last_page, 'pre_page' : page-1 , 'next_page' : page+1})


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
                # user.save()
    return render(request, 'sign_up.html')

def sign_in(request, is_submitting=False):
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
            if is_submitting:
                return redirect(request.path)
            else:
                return problem_list(request, 1)
        else:
            error = {"msg": "The name or password is incorrect."}
            return render(request, 'sign_in.html', error)

    def form_not_vaild():
        inputedData = {}
        inputedData["name"] = request.POST.get("name", "")
        inputedData["password"] = request.POST.get("password", "")
        return render(request, 'sign_in.html', {'input': inputedData})

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            return form_vaild()
        else:
            return form_not_vaild()
    else:
        if is_submitting:
            return render(request, 'sign_in.html')
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

def log_out(request):
    logout(request)
    return render(request, 'index.html')

def index(request):
    return render(request, 'index.html')
