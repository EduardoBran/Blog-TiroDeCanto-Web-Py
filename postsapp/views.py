from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from postsapp.models import Post


class PostIndex(ListView):
    model = Post
    template_name = 'postsapp/index.html'
    paginate_by = 6
    context_object_name = 'posts'
    
        
    
