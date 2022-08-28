from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.sobreView, name='sobre'),
    path('contato/', views.contatoView, name='contato'),
]
