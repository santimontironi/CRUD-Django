from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.db import IntegrityError
from .models import Task
from .forms import TaskForm
from django.utils import timezone
# Create your views here.


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]: #verificacion de si ambas claves son iguales
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save() #se guarda el usuario en la base de datos
                login(request,user) #se inicia sesion automaticamente al registrar al usuario
                return redirect('tasks')
            except IntegrityError: #IntegrityError captura excepciones solamente de la base de datos
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "errorUser": "User already exists"},
                )
        else:
            return render(
                request,
                "signup.html",
                {"form": UserCreationForm, "errorPasswords": "Passwords not match"},
            )


def signIn(request):
    if request.method == "GET":
        return render(request,'signIn.html',{
            'form':AuthenticationForm
        })
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password']) #authenticate() busca en la base de datos si hay un usuario con el username y password proporcionados.
        if user is None:
            return render(request,'signIn.html',{
                'form':AuthenticationForm,
                'error': 'Username or password incorrect'
            })
        else:
            login(request,user)
            return redirect('tasks')


def createTasks(request):
    if request.method == "GET":
        return render(request,'create_tasks.html',{
            'form': TaskForm()
        })
    else:
        try:
            data = TaskForm(request.POST)
            newTask = data.save(commit = False) #commit false es para no guardar los datos en la base de datos.
            newTask.user = request.user #request.user es la cookie del usuario autenticado
            newTask.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'create_tasks.html',{
                'form': TaskForm(),
                'error': 'Please send valid data'
            })

def tasks(request):
    if request.method == "GET":
        tasks = Task.objects.filter(user=request.user,datecompleted__isnull = True)
        return render(request,'tasks.html',{
            'tasks':tasks
        })
    
def taskDetail(request,task_id):
    if request.method == "GET":
        task = get_object_or_404(Task,id=task_id)
        form = TaskForm(instance=task) #instance en GET muestra los datos precargados de la tarea
        return render(request,'taskDetail.html',{
            'task':task,
            'form':form
        })
    else:
        try:
            task = get_object_or_404(Task,id=task_id)
            form = TaskForm(request.POST,instance=task) #instance en POST actualiza los datos de la tarea
            form.save()
            return redirect('tasks')
        except ValueError:
            error = "Hubo un error al actualizar la tarea."
            return render(request,'taskDetail.html',{
                'error':error,
                'form':form,
                'task':task
            })
            
def taskCompleted(request,task_id):
    task = get_object_or_404(Task,id=task_id)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    
def taskEliminated(request,task_id):
    task = get_object_or_404(Task,id=task_id)
    if request.method == "POST":
        task.delete()
        return redirect('tasks')

def logOut(request):
    logout(request)
    return redirect('home')