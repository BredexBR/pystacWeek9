# Pystack Week 9.0

## Introdução
O projeto a seguir se trata de um código desenvolvido a partir de um evento "Pystack week 9.0". No mesmo o fundamento principal abordado é a linguagem de programação "Python" com o framework "Django".

No programa é possível fazer cadastro de login, entrar com um usuário e criar flashcards para estudos, iniciar desafios com os flashcards cadastrados para responde-los, estatísticas em forma de relatório com os acertos e erros. E iniciar apostilas de estudos dentro da plataforma. 

## Bibliotecas/Ferramentas
Foram necessário baixar algumas bibliotecas:

A biblioteca django:
> $ pip install django

A biblioteca pillow:
> $ pip install pillow

## Configurações
Será necessário ter um banco de dados com as informações do flashCard e dos usuários(no caso do evento foi utilizado db.sqlite3), fora as dependências do Django.
para executar o projeto, basta entrar na pasta raiz e inserir no terminal:
> $ python manage.py runserver
