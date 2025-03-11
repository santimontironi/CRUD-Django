from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta: # Configuración del formulario basada en el modelo Task
        model = Task  # Le decimos a Django que este formulario está basado en Task
        fields = ['title','description','important'] #Estos son los campos que se muestran en el frontend
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'important': 'Importante'
        } #se modifican los label de cada input
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control','rows':5})
        } #se agregan estilos para poder mostrar correctamente estilizado el formulario en la intefaz