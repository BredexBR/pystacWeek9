from django.shortcuts import render, redirect
from .models import Apostila, ViewApostila
from django.contrib.messages import constants
from django.contrib import messages
from django.http import Http404

def adicionar_apostilas(request):
    if not request.user.is_authenticated:
        messages.add_message(
            request, constants.ERROR, 'Usuário não autenticado, sera necessário fazer login novamente.'
        )
        return redirect('/usuarios/logar')
    
    else:
        if request.method == 'GET':
            apostilas = Apostila.objects.filter(user=request.user)
            views_totais = ViewApostila.objects.filter(apostila__user = request.user).count()
            return render(request, 'adicionar_apostilas.html', {'apostilas': apostilas, 'views_totais': views_totais})
        elif request.method == 'POST':
            titulo = request.POST.get('titulo')
            arquivo = request.FILES['arquivo']

            apostila = Apostila(
                user=request.user, 
                titulo=titulo, 
                arquivo=arquivo
            )

            apostila.save()
            messages.add_message(
                request, constants.SUCCESS, 'Apostila adicionada com sucesso.'
            )
            return redirect('/apostilas/adicionar_apostilas/')
    
def apostila(request, id):
    if not request.user.is_authenticated:
        messages.add_message(
            request, constants.ERROR, 'Usuário não autenticado, sera necessário fazer login novamente.'
        )
        return redirect('/usuarios/logar')
    
    else:        
        apostila = Apostila.objects.get(id=id)
        views_unicas = ViewApostila.objects.filter(apostila=apostila).values('ip').distinct().count()
        views_totais = ViewApostila.objects.filter(apostila=apostila).count()

        if request.method == 'GET':
            view = ViewApostila(
                ip=request.META['REMOTE_ADDR'], #Essa função retorna o ip do usuário que esta utilizando a função
                apostila=apostila
            )
            view.save()
            return render(request, 'apostila.html', {'apostila': apostila, 
                                                    'views_unicas': views_unicas, 
                                                    'views_totais': views_totais})
        
        elif request.method == 'POST':
            avalie = request.POST.get('avalie')
            apostila.avaliacao = avalie
            apostila.save()

            return render(request, 'apostila.html', {'apostila': apostila, 
                                                    'views_unicas': views_unicas, 
                                                    'views_totais': views_totais})

def deletar_apostila(request, id):
    if not request.user.is_authenticated:
        messages.add_message(
            request, constants.ERROR, 'Usuário não autenticado, sera necessário fazer login novamente.'
        )
        return redirect('/usuarios/logar')
    else:
        apostila = Apostila.objects.get(id=id)
        
        if not apostila.user == request.user:
                raise Http404()
        
        apostila.delete()
        messages.add_message(
        request, constants.SUCCESS, 'Desafio deletado com sucesso!'
        )
        return redirect() 
