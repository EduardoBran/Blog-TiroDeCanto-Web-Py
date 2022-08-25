from categorias.models import Categoria
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        qs = qs.order_by('data_post').filter(publicado_post=True)
        qs = qs.annotate(
            numero_comentarios=Count(
                Case(
                    When(comentario__publicacao_comentario=True, then=1)
                )
            )
        )    
        return qs


class PostBusca(PostIndex):
    template_name = 'postsapp/post_busca.html'        


class PostCategoria(PostIndex):
    template_name = 'postsapp/post_categoria.html'    
