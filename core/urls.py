from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Página inicial redirecionada para login
    path('conta/', views.conta, name='conta'),
    path('api/login/', views.login_api, name='login_api'),
    path('update_data/', views.update_data),
]