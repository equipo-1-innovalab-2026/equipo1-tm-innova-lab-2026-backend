from django.urls import path
from .views import api_login

urlpatterns = [
    path('login/', api_login, name='api_login'),
]