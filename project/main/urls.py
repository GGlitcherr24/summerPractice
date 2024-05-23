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
    path('<int:age>', show_age, name='show_age'),
    path('main/<int:age>', show_age, name='show_age'),
    path('gender/<int:gender_id>/<int:age>', show_age, name='show_age'),
    path('addpage', addpage, name='addpage'),
    path('my_anket', my_anket, name='my_anket'),
    path('delete_anket', delete_anket, name='delete_anket'),
    path('team', team, name='team'),
    path('contacts', contacts, name='contacts'),
    path('main/search', find_bad_content, name='find_bad_content'),
    path('post/<slug:post_slug>/<slug:slug_post_one>', admin_delete_account, name='admin_delete_account'),
    path('quesiton', question_for_admin, name='question_for_admin'),
    path('question/submit', send_question, name='send_question'),
    path('main/<hobby>', filter_hobby, name='filter_hobby'),
    path('gender/<int:gender_id>/<hobby>', filter_hobby_and_gender_id, name='filter_hobby_and_gender_id'),
    path('main/<int:age>/<hobby>', filter_hobby_and_age, name='filter_hobby_and_age'),
    path('gender/<int:gender_id>/<int:age>/<str:hobby>', filter_hobby_age_gender, name='filter_hobby_age_gender')
]