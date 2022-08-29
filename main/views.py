from categorias.models import Categoria
from django.shortcuts import render


def sobreView(request):
    categorias =  Categoria.objects.order_by('nome_cat')
    context = {
        'categorias': categorias
    }
    return render(request, 'main/sobre.html', context)


def contatoView(request):
    return render(request, 'main/contato.html')
