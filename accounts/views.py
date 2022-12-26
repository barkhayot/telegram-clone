from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from . forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required



# Create your views here.

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account successfully has been created')
            return redirect('loginpage')
    context = {
        'form': form,
    } 
    return render(request, 'accounts/register.html', context)

def loginpage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')

        user = authenticate(request, username=username, password=password)
        
        if user is not None :
            login(request, user)
            return redirect('getChats')
        else:
            messages.info(request, 'Username or Password is incorrect')

    return render(request, 'accounts/login.html' )

@login_required(login_url='loginpage')
def logoutpage(request):
    logout(request)
    return redirect('loginpage')



@login_required(login_url='loginpage')
def home(request):
    return render(request, 'accounts/home.html')