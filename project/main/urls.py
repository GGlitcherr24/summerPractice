from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('main/', main, name='main'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', Logout_User, name='logout')
]