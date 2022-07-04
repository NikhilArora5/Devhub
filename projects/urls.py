from . import views as project_views
from django.contrib import admin
from django.urls import path,include



urlpatterns = [
    path('',project_views.projects,name='projects'),
    path('create-project/',project_views.create_project,name='create-project'),
    path('update-project/<str:pk>/',project_views.update_project,name='update-project'),
    path('delete-project/<str:pk>/',project_views.delete_project,name='delete-project'),
    path('view-project/<str:pk>/',project_views.single_project,name='view-project')
]