from django.urls import path
from .views import login_motorista

urlpatterns = [
    path('login_motorista/', login_motorista, name='login_motorista'),
]
