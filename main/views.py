from categorias.models import Categoria
from django.contrib import messages
from django.shortcuts import render

from .forms import ContatoForm


def sobreView(request):
    categorias =  Categoria.objects.order_by('nome_cat')
    context = {
        'categorias': categorias
    }
    return render(request, 'main/sobre.html', context)


def contatoView(request):
    
    if str(request.method) == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.send_email()
            messages.success(request, 'E-mail enviado com sucesso.')
            form = ContatoForm()
        else:
            messages.error(request, 'E-mail NÃO foi enviado.')
    else:
        form = ContatoForm()
    
    categorias =  Categoria.objects.order_by('nome_cat')
    context = {
        'form': form,
        'categorias': categorias
    }
    return render(request, 'main/contato.html', context)
