from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required
import hashlib

# Create your views here.

@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        if request.POST.get('select'):
            select = todo.hash_code
            select = request.POST.get('select')
            h = hashlib.new(select)
            h.update(str.encode(task))
            select = h.hexdigest()
            

        new_todo = todo(user=request.user, todo_name=task, hash_code=select)
        new_todo.save()

    all_todos = todo.objects.filter(user=request.user)
    context= {
        'todos': all_todos
    }
    return render(request, 'Almacenamiento/Todolist.html',context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password)<3:
            messages.error(request, "La contraseña debe tener al menos 3 caracteres.")
            return redirect('register')
        
        get_all_user_by_username = User.objects.filter(username=username)
        if get_all_user_by_username:
            messages.error(request, "Error, nombre de usuario ya existe, ingresa otro usuario que no exista.")
            return redirect('register')

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        messages.success(request, 'Usuario creado correctamente, inicie sesión ahora')
        return redirect('login')
    return render(request, 'Almacenamiento/Register.html',{})

def logoutView(request):
    logout(request)
    return redirect('login')

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'Error, Nombre de usuario incorrecto o el Usuario no existe')
            return redirect('login')
    return render(request, 'Almacenamiento/Login.html',{})

@login_required
def Deletetask(request, name):
    get_todo = todo.objects.filter(user=request.user, todo_name=name)
    get_todo.delete()
    return redirect('home-page')

@login_required
def Update(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')