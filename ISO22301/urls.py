from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #path("",views.user_login,),
    path("layout/", views.layout, name="layout"),
   # path("survey/", views.survey, name="survey"),
    path("results/<str:id>", views.results, name="results"),
    path('login/', views.user_login, name='login'),
    path('generic/', views.generic, name='generic'),
    path('introduction<str:id>', views.introduction, name='introduction'),
    path('goodbye/', views.user_logout, name='goodbye'),
    path('wheel/', views.wheel, name='wheel'),
]