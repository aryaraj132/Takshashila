from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from users.forms import UserForm, CustomUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request,'index.html')

    

def register(request):
    registed = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        custom_form = CustomUserForm(data=request.POST)
        if user_form.is_valid() and custom_form.is_valid():
            user = user_form.save()
            user.save()

            custom = custom_form.save(commit=False)
            custom.user = user
            custom.save()

            registed = True
            return HttpResponseRedirect(reverse('login'))
        else:
            print(user_form.errors, custom_form.errors)
    else:
        user_form = UserForm()
        custom_form = CustomUserForm

    return render(request, 'users/register.html',
                  {'registed': registed,
                   'user_form': user_form,
                   'custom_form': custom_form
                   })


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user =authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect('index')
            else:
                return HttpResponse("ACCOUNT IS DEACTIVATED")
        else:
            return HttpResponse("Please Use Correct Username and Password")
    else:
        return render(request,'users/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))