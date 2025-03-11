from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.db import IntegrityError
from .models import Task
from .forms import TaskForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html")
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
                    {"errorUser": "Error. Un usuario ya existe con ese nombre."},
                )
        else:
            return render(
                request,
                "signup.html",
                {"errorPasswords": "Error. Las contraseñas no coinciden."},
            )

def signIn(request):
    if request.method == "GET":
        return render(request,'signIn.html')
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password']) #authenticate() busca en la base de datos si hay un usuario con el username y password proporcionados.
        if user is None:
            return render(request,'signIn.html',{
                'error': 'Usuario o contraseñas incorrectos.'
            })
        else:
            login(request,user)
            return redirect('tasks')

@login_required
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
            
@login_required
def tasks(request):
    if request.method == "GET":
        tasks = Task.objects.filter(user=request.user,datecompleted__isnull = True)
        if tasks:
            return render(request,'tasks.html',{
                'tasks':tasks
            })
        else:
            return render(request,'tasks.html',{
                'noTasks': 'No hay tareas pendientes.'
            })
    
@login_required   
def taskDetail(request,task_id):
    if request.method == "GET":
        task = get_object_or_404(Task,id=task_id)
        form = TaskForm(instance=task) #instance en GET muestra los datos precargados de la tarea
        return render(request,'taskDetail.html',{
            'task':task,
            'form':form
        })
    else:
        task = get_object_or_404(Task,id=task_id)
        form = TaskForm(request.POST,instance=task) #instance en POST actualiza los datos de la tarea
        form.save()
        return redirect('tasks')

            
@login_required
def taskCompleted(request,task_id):
    task = get_object_or_404(Task,id=task_id)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    
@login_required
def taskEliminated(request,task_id):
    task = get_object_or_404(Task,id=task_id)
    if request.method == "POST":
        task.delete()
        return redirect('tasks')

@login_required    
def tasksCompleted(request):
    if request.method == "GET":
        tasks = Task.objects.filter(user=request.user,datecompleted__isnull = False)
        return render(request,'tasksCompleted.html',{
            'tasks':tasks
        })

@login_required
def logOut(request):
    logout(request)
    return redirect('home')