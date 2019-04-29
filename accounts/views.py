from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import UserCustomCreationForm

# Create your views here.
def mainpage(request):
	form = UserCreationForm()
	
	return render(request, 'accounts/mainpage.html', {
		'form':form,
	})

def signup(request):
    #회원 가입
    if request.method == "POST":
        form = UserCustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('mainpage')
    else:
        form = UserCustomCreationForm()
        
    return render(request, 'accounts/signup.html', {
        'form':form,
    })
    
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return render(request, 'accounts/mainpage.html')
        else:
            return redirect('accounts:login')
    else:
        #유저로부터 username 과 비밀번호를 받는다.
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {
            'form':form,
        })

def logout(request):
    auth_logout(request)
    return redirect('mainpage')