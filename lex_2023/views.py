import asyncio

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from lex_2023.bot import main
from lex_2023.models import Modellex2023


# Create your views here.
@csrf_exempt
def index(request):
    if request.method == 'POST':
        print('Bot Started')
        asyncio.run(main()) #запуск бота

    return render(request,'index.html')
#@csrf_exempt
#def home(request):
    #if request.method == 'GET':
        #return render(request,'home.html',{'user':'super page'})
   # if request.method == 'POST':
      #  loginn = request.POST['login']
      #  password = request.POST['password']
      #  emaill = request.POST['email']
       # print(loginn,password,emaill)
      #  return HttpResponse(f'Авторизация прошла успешно\nLogin:{loginn} Password:{password} Email:{emaill}')
   # return HttpResponse('Такой запрос непредусмотрен')
@csrf_exempt
def home(request):
    home = Modellex2023()


    if request.method == 'POST':
        data = Modellex2023.objects.all()
        for i in data:
            if request.POST['email'] == i.email: return render(request, 'home.html', {"err": "Данный Email занят"})
        if len(request.POST['password']) < 6: return render(request, 'home.html', {"err": "Пароль слишком короткий"})
        home.pole = 'Hello world'
        home.email = request.POST['email']
        home.password = request.POST['password']
        home.save()
        return HttpResponse('Email'+' '+home.email+' '+"успешно зарегистрирован!")

    return render(request, 'home.html', {"err": ""})