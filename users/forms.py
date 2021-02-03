from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import profile

class UserForm(UserCreationForm):
    email = forms.EmailField()
    class Meta():
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')
        labels = {
            'password1' : 'Password',
            'password2' : 'Confirm Password'
        }

class CustomUserForm(forms.ModelForm):
    # teacher = 'teacher'
    # student = 'student'
    # user_types = [
    #     (student,'student')
    # ]
    # user_type = forms.CharField(choices = user_types,required=True)
    class Meta():
        model = profile
        fields = ('branch','dp','semester')