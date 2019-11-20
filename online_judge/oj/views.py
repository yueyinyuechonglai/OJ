from django.shortcuts import render
from django.http import HttpResponse
from .models import Problem
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
