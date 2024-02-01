from django.shortcuts import render, redirect
from .models import Categoria, Flashcard, Desafio, FlashcardDesafio
from django.contrib.messages import constants
from django.contrib import messages
from django.http import Http404


def novo_flashcard(request):
    if not request.user.is_authenticated:
        messages.add_message(
            request, constants.ERROR, 'Usuário não autenticado, sera necessário fazer login novamente.'
        )
        return redirect('/usuarios/logar')
    
    else:
        if request.method == 'GET':
            categorias = Categoria.objects.all()
            dificuldades = Flashcard.DIFICULDADE_CHOICES
            flashcards = Flashcard.objects.filter(user=request.user)

            categoria_filtrar = request.GET.get('categoria')
            dificuldade_filtrar = request.GET.get('dificuldade')

            if categoria_filtrar:
                flashcards = flashcards.filter(categoria__id=categoria_filtrar)

            if dificuldade_filtrar:
                flashcards = flashcards.filter(dificuldade=dificuldade_filtrar)

            return render(
                request,
                'novo_flashcard.html',
                {
                    'categorias': categorias,
                    'dificuldades': dificuldades,
                    'flashcards': flashcards,
                }
                
            )
        elif request.method == 'POST':
            pergunta = request.POST.get('pergunta')
            resposta = request.POST.get('resposta')
            categoria = request.POST.get('categoria')
            dificuldade = request.POST.get('dificuldade')

            if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
                messages.add_message(
                    request,
                    constants.ERROR,
                    'Preencha os campos de pergunta e resposta',
                )
                return redirect('/flashcard/novo_flashcard')

            flashcard = Flashcard(
                user=request.user,
                pergunta=pergunta,
                resposta=resposta,
                categoria_id=categoria,
                dificuldade=dificuldade,
            )

            flashcard.save()

            messages.add_message(
                request, constants.SUCCESS, 'Flashcard criado com sucesso'
            )
            return redirect('/flashcard/novo_flashcard')

def deletar_flashcard(request, id):
    if not request.user.is_authenticated:
        messages.add_message(
            request, constants.ERROR, 'Usuário não autenticado, sera necessário fazer login novamente.'
        )
        return redirect('/usuarios/logar')
    
    else:
        try:
            flashcard = Flashcard.objects.get(id=id)
            if not flashcard.user == request.user:
                messages.add_message(
                    request, constants.ERROR, 'Não se pode deletar flashcard criado por outro usuário!'
                )
                return redirect('/flashcard/novo_flashcard')
            else:
                print("flashcardUser" , flashcard.user) 
                flashcard.delete()
                messages.add_message(
                    request, constants.SUCCESS, 'Flashcard deletado com sucesso!'
                )
                return redirect('/flashcard/novo_flashcard')
    
        except Exception as e:
            messages.add_message(
                request, constants.ERROR, "Não foi possível encontrar o "
                "flashcard a ser deletado."
            )
            return redirect('/flashcard/novo_flashcard')    

def iniciar_desafio(request):
    if not request.user.is_authenticated:
        messages.add_message(
            request, constants.ERROR, 'Usuário não autenticado, sera necessário fazer login novamente.'
        )
        return redirect('/usuarios/logar')
    
    else:
        if request.method == 'GET':
            categorias = Categoria.objects.all()
            dificuldades = Flashcard.DIFICULDADE_CHOICES
            return render(
                request,
                'iniciar_desafio.html',
                {'categorias': categorias, 'dificuldades': dificuldades},
            )
        elif request.method == 'POST':
            titulo = request.POST.get('titulo')
            categorias = request.POST.getlist('categoria')
            dificuldade = request.POST.get('dificuldade')
            qtd_perguntas = request.POST.get('qtd_perguntas')

            if len(titulo.strip()) == 0 or len(categorias) == 0 or len(qtd_perguntas.strip()) == 0:
                messages.add_message(
                    request,
                    constants.ERROR,
                    'Preencha os campos de titulo, categoria, dificuldade e Qtd questões.',
                )
                return redirect('/flashcard/iniciar_desafio/')
            else:
                desafio = Desafio(
                    user=request.user,
                    titulo=titulo,
                    quantidade_perguntas=qtd_perguntas,
                    dificuldade=dificuldade,
                )
                desafio.save()

                for categoria in categorias:
                    desafio.categoria.add(categoria)

                flashcards = (
                    Flashcard.objects.filter(user=request.user)
                    .filter(dificuldade=dificuldade)
                    .filter(categoria_id__in=categorias) # lista de id de categorias dentro de categorias
                    .order_by('?')
                )

                if flashcards.count() < int(qtd_perguntas):
                    messages.add_message(
                        request, constants.ERROR, f"Só existem {flashcards.count()} flashcards para"
                        f" esta categoria e dificuldade. Não será possível adicionar as {qtd_perguntas} perguntas."
                    )
                    return redirect('/flashcard/iniciar_desafio/')

                flashcards = flashcards[: int(qtd_perguntas)]

                for f in flashcards:
                    flashcard_desafio = FlashcardDesafio(
                        flashcard=f,
                    )
                    flashcard_desafio.save()
                    desafio.flashcards.add(flashcard_desafio)

                desafio.save()
                #return HttpResponse("teste")
                return redirect(f'/flashcard/desafio/{desafio.id}')

def listar_desafio(request):
    if not request.user.is_authenticated:
        messages.add_message(
            request, constants.ERROR, 'Usuário não autenticado, sera necessário fazer login novamente.'
        )
        return redirect('/usuarios/logar')
    
    else:
        desafios = Desafio.objects.filter(user=request.user)
        
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES

        categoria_filtrar = request.GET.get('categoria')
        dificuldade_filtrar = request.GET.get('dificuldade')

        if categoria_filtrar:
            desafios = Desafio.objects.filter(categoria__id=categoria_filtrar)

        if dificuldade_filtrar:
            desafios = Desafio.objects.filter(dificuldade=dificuldade_filtrar)

        return render(
            request,
            'listar_desafio.html',
            {
                'desafios': desafios,
                'categorias': categorias,
                'dificuldades': dificuldades
            },
        )

def desafio(request, id):
    if not request.user.is_authenticated:
        messages.add_message(
            request, constants.ERROR, 'Usuário não autenticado, sera necessário fazer login novamente.'
        )
        return redirect('/usuarios/logar')
    
    else:
        desafio = Desafio.objects.get(id=id)

        if not desafio.user == request.user:
            raise Http404() 

        if request.method == 'GET':
            acertos = desafio.flashcards.filter(respondido=True).filter(acertou=True).count()
            erros = desafio.flashcards.filter(respondido=True).filter(acertou=False).count()
            faltantes = desafio.flashcards.filter(respondido=False).count()
            categorias = desafio.categoria.all()
            name_categoria = [i.nome for i in categorias]
            dificuldades = desafio.dificuldade

            return render(
                request,
                'desafio.html',
                {
                    'desafio': desafio,
                    'acertos': acertos,
                    'erros': erros,
                    'faltantes': faltantes,
                    'categorias': name_categoria,
                    'dificuldades': dificuldades,
                },
            )

def deletar_desafio(request, id):
    if not request.user.is_authenticated:
        messages.add_message(
            request, constants.ERROR, 'Usuário não autenticado, sera necessário fazer login novamente.'
        )
        return redirect('/usuarios/logar')
    else:
        desafio = Desafio.objects.get(id=id)
        
        if not desafio.user == request.user:
                raise Http404()
        
        desafio.delete()
        messages.add_message(
        request, constants.SUCCESS, 'Desafio deletado com sucesso!'
        )
        return redirect('/flashcard/listar_desafio') 

def responder_flashcard(request, id):
    if not request.user.is_authenticated:
        messages.add_message(
            request, constants.ERROR, 'Usuário não autenticado, sera necessário fazer login novamente.'
        )
        return redirect('/usuarios/logar')
    
    else:
        flashcard_desafio = FlashcardDesafio.objects.get(id=id)
        acertou = request.GET.get('acertou')
        desafio_id = request.GET.get('desafio_id')

        if not flashcard_desafio.flashcard.user == request.user:
            raise Http404()

        flashcard_desafio.respondido = True
        flashcard_desafio.acertou = True if acertou == '1' else False # flashcard é true se a variavel acertou é igual a 1 se não é falso
        flashcard_desafio.save()

        desafio = Desafio.objects.get(id=desafio_id)
        desafio_flashcards = desafio.flashcards.all().count()
        desafio_flashcards_respondidos = desafio.flashcards.filter(
            respondido=True
        ).count()

        if desafio_flashcards_respondidos == desafio_flashcards:
            desafio.status = True
            desafio.save()

        return redirect(f'/flashcard/desafio/{desafio_id}/')

def relatorio(request, id):
    if not request.user.is_authenticated:
        messages.add_message(
            request, constants.ERROR, 'Usuário não autenticado, sera necessário fazer login novamente.'
        )
        return redirect('/usuarios/logar')
    
    else:
        desafio = Desafio.objects.get(id=id)

        acertos = desafio.flashcards.filter(acertou=True).count()
        erros = desafio.flashcards.filter(acertou=False).count()

        dados = [acertos, erros]

        categorias = desafio.categoria.all()
        name_categoria = [i.nome for i in categorias]

        dados2 = []
        for categoria in categorias:
            dados2.append(desafio.flashcards.filter(flashcard__categoria=categoria).filter(acertou=True).count())
            
        resultados_por_categoria = {}
        for categoria in categorias:
            resultados_por_categoria[f"{categoria}"] = {
                "acertos": (
                    desafio.flashcards.filter(flashcard__categoria=categoria)
                    .filter(acertou=True)
                    .count()
                )
            }
            resultados_por_categoria[f"{categoria}"]["erros"] = (
                desafio.flashcards.filter(flashcard__categoria=categoria)
                .filter(acertou=False)
                .count()
            )
        
        return render(request, 'relatorio.html', {'desafio': desafio, 'dados': dados, 
                                                'categorias': name_categoria, 'dados2': dados2,                                              
                                                "resultados_por_categoria": resultados_por_categoria,},)