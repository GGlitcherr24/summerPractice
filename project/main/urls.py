from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('main/', main, name='main'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', show_post, name='post'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', Logout_User, name='logout'),
    path('gender/<int:gender_id>/', show_gender, name='gender'),
    path('addpage', addpage, name='addpage'),
    path('my_anket', my_anket, name='my_anket'),
    path('delete_anket', delete_anket, name='delete_anket'),
    path('team', team, name='team'),
    path('contacts', contacts, name='contacts')
]