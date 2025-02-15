from django.contrib import admin 
from django.urls import path
from django.contrib.auth import views as auth_views
from turing_app import views  

urlpatterns = [
    path('admin/', views.admin_panel, name='admin_panel'),
    path('', views.index, name='index'),
    path('submit-question/', views.submit_question, name='submit_question'),
    path('answer-question/', views.answer_question, name='answer_question'),
    path('get_latest-response/', views.get_latest_response, name='get_latest_response'),
    path('vote-question/', views.vote_question, name='vote_question'),

    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]
