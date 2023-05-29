from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('logout', signout, name="logout"),
    path('login', signin, name="loginpage"),
    path('settings', settings, name="settings"),
    path('result', matchResult, name="matchresult"),
    path('search', searchPage.as_view(), name="searchPage"),
    # path('test', calTest, name="test"),
    path('test', testPage, name="test"),
    path('addtask', addTask, name="addTask"),
    path('player/<slug>', getPlayer, name="getPlayer"),
    path('user/setting', userSettings, name="userSettings"),
]