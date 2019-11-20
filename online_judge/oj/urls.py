from django.urls import path

from . import views

urlpatterns = [
    path('problems/p<int:page>/',views.problem_list,name='problem_list'),
    path('problem/<int:prob_id>/', views.prob_detail, name='prob_detail'),
    path('submit/',views.submit,name='submit')
]
