"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('signup/',views.signup, name='signup'),
    path('signIn/',views.signIn, name='signIn'),
    path('createTasks/',views.createTasks, name='createTask'),
    path('tasks/',views.tasks, name='tasks'),
    path('tasks/<int:task_id>/',views.taskDetail, name='taskDetail'),
    path('task/completed/<int:task_id>',views.taskCompleted, name='taskCompleted'),
    path('task/eliminated/<int:task_id>',views.taskEliminated, name='taskEliminated'),
    path('logout/',views.logOut, name='logout')
]
