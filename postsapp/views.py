from django.db.models import Case, Count, Q, When
from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from postsapp.models import Post


class PostIndex(ListView):
    model = Post
    template_name = 'postsapp/index.html'
    paginate_by = 6
    context_object_name = 'posts'
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        qs = qs.order_by('data_post')
        qs = qs.annotate(
            numero_comentarios=Count(
                Case(
                    When(comentario__publicacao_comentario=True, then=1)
                )
            )
        )    
        return qs
        
    
