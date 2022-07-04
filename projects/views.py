import profile
from django.shortcuts import redirect, render
from .models import Project

from .forms import ProjectForm,ReviewForm

from django.contrib import messages
# Create your views here.

from. utils import searchProjects

def projects(request):
    projects, search_query = searchProjects(request)
    # custom_range, projects = paginateProjects(request, projects, 6)

    context = {'projects': projects,
               'search_query': search_query}
    return render(request,'project.html',context)


def single_project(request,pk):
    project_obj=Project.objects.get(id=pk)
    profile=request.user
    form=ReviewForm()

    if request.method=='POST':
        form=ReviewForm(request.POST)
        
        if form.is_valid():
            review=form.save(commit=False)
            review.owner=profile

            review.project=project_obj
            
            

            print(f'count {project_obj}')
            review.save()
            project_obj.getVoteCount

            messages.success(request, 'Your review was successfully submitted!')
            
            return redirect('view-project',pk=project_obj.id)


          
    
    
    context={'project':project_obj,'form':form}
    
    return render(request,'projects/view_project.html',context)





def create_project(request):
    profile=request.user
    form=ProjectForm()
    
    if request.method=='POST':
        form=ProjectForm(request.POST,request.FILES)
        
        if form.is_valid():
            project=form.save(commit=False)
            project.owner=profile
            

            project.save()
            
            return redirect('projects')        
    
    
    context={'form':form}
    
    return render(request,'projects/project_form.html',context)


def update_project(request,pk):
    project=Project.objects.get(id=pk)
    form=ProjectForm(instance=project)
    
    if request.method=='POST':
        form=ProjectForm(request.POST,request.FILES,instance=project)
        
        if form.is_valid():
            form.save()
            
            return redirect('projects')        
    
    
    context={'form':form}
    
    return render(request,'projects/project_form.html',context)



def delete_project(request,pk):
    project=Project.objects.get(id=pk)
    # form=ProjectForm(instance=project)
    
    if request.method=='POST':
        project.delete()
            
        return redirect(projects)       
    
    
    context={'object':project}
    
    return render(request,'delete.html',context)

    

    