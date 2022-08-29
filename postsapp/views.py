from categorias.models import Categoria
from comentarios.forms import FormComentario
from comentarios.models import Comentario
from django.contrib import messages
from django.db.models import Case, Count, Q, When
from django.shortcuts import redirect, render
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
            messages.warning(self.request, f'Não foi digitada nenhuma palavra para busca.')
            return qs
        
        qs = qs.filter(
            Q(titulo_post__icontains=termo) |
            Q(autor_post__first_name__iexact=termo) |
            Q(conteudo_post__icontains=termo) |
            Q(excerto_post__icontains=termo) |
            Q(categoria_post__nome_cat__iexact=termo)
        )
        
        messages.success(self.request, f'Buscando pela(s) palavra(s): "{termo}"')
        
        return qs


class PostCategoria(PostIndex):
    template_name = 'postsapp/post_categoria.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        categoria = self.kwargs.get('categoria', None)
        
        if not categoria:
            return qs
        
        qs = qs.filter(categoria_post__nome_cat__iexact=categoria)
        
        if qs.count() >= 1 :
            messages.success(self.request, f'Buscando posts pela categoria: "{categoria}"')
        else:
            messages.warning(self.request, f'Ainda não temos nenhum post cadastrado na categoria: "{categoria}"')
        
        return qs


class PostDetalhes(UpdateView, PostIndex):
    template_name = 'postsapp/post_detalhes.html'
    model = Post
    form_class = FormComentario
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        
        post = self.get_object()
        comentarios = Comentario.objects.filter(publicacao_comentario=True,
                                                post_comentario=post.id
                                                )
        contexto['comentarios'] = comentarios
        
        return contexto
    
    def form_valid(self, form):
        post = self.get_object()
                
        comentario = Comentario(**form.cleaned_data)
        comentario.post_comentario = post
        
        if self.request.user.is_authenticated:
            comentario.usuario_comentario = self.request.user
        
        comentario.save()
        messages.success(self.request, f'Seu comentário foi enviado com sucesso.')
        return redirect('postsapp:post_detalhes', pk=post.id)
