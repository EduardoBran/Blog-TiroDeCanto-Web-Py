from django.urls import path

from . import views

app_name = 'postsapp'

urlpatterns = [
    path('', views.PostIndex.as_view(), name='index')
]
