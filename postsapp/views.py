from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView


class PostIndex(TemplateView):
    template_name = 'postsapp/index.html'

    
