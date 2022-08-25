from categorias.models import Categoria
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Post(models.Model):
    titulo_post = models.CharField(max_length=100, verbose_name='Título')
    autor_post = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Autor')
    data_post = models.DateTimeField(default=timezone.now, verbose_name='Data')
    conteudo_post = models.TextField(verbose_name='Conteúdo')
    excerto_post = models.TextField(verbose_name='Excerto')
    categoria_post = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, blank=True, null=True)
    imagem_post = models.URLField(blank=True, null=True)
    publicado_post = models.BooleanField(default=False)
    