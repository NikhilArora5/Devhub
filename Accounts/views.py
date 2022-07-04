import email
from multiprocessing import context
import profile
from re import A
from django.shortcuts import render
from django.shortcuts import redirect, render

from .models import Account,skill
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import conf
from django.db.models import Q
from .models import  Message
from .forms import CustomUserCreationForm,ProfileForm,SkillForm
from .utils import searchProfiles

from allauth.account.views import LoginView

# def CustomLoginview(LoginView):

from django.contrib.auth import get_user_model

Account=get_user_model()




def profiles(request):
    search_query=''

    profiles, search_query = searchProfiles(request)

    context={'profiles':profiles,'search_query':search_query}    

    return render(request,'accounts/profiles.html',context)


def single_profile(request,pk):
    profile=Account.objects.get(id=pk)
    topskills=profile.skill_set.exclude(description=None)
    otherskills=profile.skill_set.filter(description=None)
    projects=profile.project_set.all()
    context={'profile':profile,'topskills':topskills,'otherskills': otherskills ,'projects':projects}
    print(topskills)

    print(projects)

    return render(request,'accounts/single-profile.html',context)




# Create your views here.




def loginUser(request):
    page = 'login'
    context={page:'page'}

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        print(email)

        try:
            user = Account.objects.get(email=email)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'you have succesully logged in')
            
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')

        else:
            messages.error(request, 'Username OR password is incorrect')
        

    return render(request, 'accounts/login_register.html',context)

def registerUser(request):
    page='register'
    form=CustomUserCreationForm()
    context={'page':page,'form':form}

    if request.method=='POST':
        form=CustomUserCreationForm(request.POST)

        if form.is_valid():
            user=form.save(commit=False)
            user.email =user.email.lower()
            user.name=user.name.lower()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('profiles')

        else:
            messages.success(
                request, 'An error has occurred during registration')

    return render(request, 'accounts/login_register.html',context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')

@login_required
def userAccount(request):
    profile=request.user  
    skills=profile.skill_set.all()
    # otherskills=profile.skill_set.filter(description=None)
    projects=profile.project_set.all()

    print(projects)


    context={'profile':profile,'skills':skills,'projects':projects}

    return render(request,'accounts/account.html',context)


def editAccount(request):
    profile=request.user

    form=ProfileForm(instance=profile)

    if request.method=='POST':
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()

            redirect('account')

    context={'form':form}

    


    return render(request,'accounts/profile_form.html',context)



def createSkill(request):
    profile=request.user
    form=SkillForm()

    if request.method=='POST':
        form=SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            print(f'profile is {profile}')
            messages.success(request, 'Skill was added successfully!')
            return redirect('account')


    
    context={'form':form}

    return render(request,'accounts/skill_form.html',context)


def updateSkill(request,pk):
    profile=request.user
    skill=profile.skill_set.get(id=pk)
    form=SkillForm(instance=skill)

    if request.method=='POST':
        form=SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()

            messages.success(request, 'Skill was updated successfully!')
            return redirect('account')
      
    context={'form':form}
    return render(request,'accounts/skill_form.html',context)




def deleteSkill(request,pk):
    profile = request.user
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete.html', context)




