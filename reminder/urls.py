from django.urls import path
from . import views
from .views import custom_logout_view

urlpatterns = [
    path('home/', views.home, name='home'),
    path('create-reminder/', views.create_reminder, name='create_reminder'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', custom_logout_view, name='logout'),
]
