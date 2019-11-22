from django.urls import path

from . import views

urlpatterns = [
    path('', views.sign_in, name='index'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('problems/p<int:page>/',views.problem_list,name='problem_list'),
    path('problem/<int:prob_id>/', views.prob_detail, name='prob_detail'),
    path('submit/',views.submit, name='submit')
]
