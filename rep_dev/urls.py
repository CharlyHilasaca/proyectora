from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='login/'), name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('vistapl/', views.vistapl, name='vistapl'),
    path('vistapl/<str:ruta>/', views.vistads, name='vistads'),
    path('logout/', views.logout, name='logout'),
]
