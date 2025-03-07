from django.forms import ModelForm
from .models import Task

class TaskForm(ModelForm):
    class Meta: # Configuración del formulario basada en el modelo Task
        model = Task  # Le decimos a Django que este formulario está basado en Task
        fields = ['title','description','important'] #Estos son los campos que se muestran en el frontend