from django.shortcuts import render


def sobreView(request):
    return render(request, 'main/sobre.html')


def contatoView(request):
    return render(request, 'main/contato.html')
