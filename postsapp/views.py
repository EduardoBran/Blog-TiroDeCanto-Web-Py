from categorias.models import Categoria
from comentarios.forms import FormComentario
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
    
    def get_queryset(self):
        qs = super().get_queryset()
        termo = self.request.GET.get('termo')
        
        if not termo:
            return qs
        
        qs = qs.filter(
            Q(titulo_post__icontains=termo) |
            Q(autor_post__first_name__iexact=termo) |
            Q(conteudo_post__icontains=termo) |
            Q(excerto_post__icontains=termo) |
            Q(categoria_post__nome_cat__iexact=termo)
        )
        
        return qs


class PostCategoria(PostIndex):
    template_name = 'postsapp/post_categoria.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        categoria = self.kwargs.get('categoria', None)
        
        if not categoria:
            return qs
        
        qs = qs.filter(categoria_post__nome_cat__iexact=categoria)
        
        return qs


class PostDetalhes(UpdateView):
    template_name = 'postsapp/post_detalhes.html'
    model = Post
    form_class = FormComentario
    context_object_name = 'post'

