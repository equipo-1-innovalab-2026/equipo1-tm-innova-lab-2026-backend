from django.urls import path
from .views import api_login, api_register, api_logout

urlpatterns = [
    path('login/', api_login, name='api_login'),
    path('register/', api_register, name='api_register'),
    path('logout/', api_logout, name='api_logout'),
]