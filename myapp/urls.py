from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='index'),
    path('home/',views.home,name='home'),
    path('create/',views.create,name='create'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('vote/<question_id>/',views.vote,name='vote'),
    path('result/<question_id>/',views.result,name='result'),
     path('saveuser/',views.saveuser,name='saveuser'),
    path('createpoll/',views.createpoll,name='createpoll'),
    path('savevote/',views.savevote,name='savevote')
]
