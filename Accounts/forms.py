from curses import meta
from pyexpat import model
from allauth.account.forms import SignupForm,LoginForm
from django import forms
from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm

from .models import Account,skill




from cProfile import label
from enum import unique
from unittest.util import _MAX_LENGTH
from allauth.account.forms import SignupForm
from django import forms
 
# class CustomLoginForm(LoginForm):
#     email = forms.EmailField(label='Email')
#     password= forms.PasswordInput()
 
#     def save(self, request):
#         user = super(CustomSignupForm, self).save(request)
#         user.email = self.cleaned_data['email']
#         user.password = self.cleaned_data['password']
#         user.save()
#         return user

 
class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=30, label=' Name',)
    bio= forms.CharField(max_length=10, required=False)
 
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.bio = self.cleaned_data['bio']
        user.save()
        return user

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['name', 'email', 'password1', 'password2']
        labels = {
            'name': 'Name',
            'email':'E-mail'
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'email',
                  'location', 'bio', 'short_intro', 'profile_image',
                  'social_github', 'social_linkedin', 'social_twitter',
                  'social_youtube', 'social_website']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class SkillForm(ModelForm):
    class Meta:
        model = skill
        exclude =['owner']
        fields = ['name','description']
        

#     def __init__(self, *args, **kwargs):
#         super(SkillForm, self).__init__(*args, **kwargs)

#         for name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'input'})


# class MessageForm(ModelForm):
#     class Meta:
#         model = Message
#         fields = ['name', 'email', 'subject', 'body']

#     def __init__(self, *args, **kwargs):
#         super(MessageForm, self).__init__(*args, **kwargs)

#         for name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'input'})




