from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #path("",views.user_login,),
   # path("layout/", views.layout, name="layout"),
   # path("survey/", views.survey, name="survey"),
    path("results/<str:id>", views.results, name="results"),
    path('login/', views.user_login, name='login'),
    path('generic/', views.generic, name='generic'),
    path('introduction<str:id>', views.introduction, name='introduction'),
    path('ISO22301/logout/', views.user_logout, name='logout'),
    path('wheel/', views.wheel, name='wheel'),
    path('results_overall/', views.results_overall, name='results_overall',)
]