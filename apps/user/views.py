from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import ListChars
from .forms import CharacterSelectionForm 
from django.contrib.auth.decorators import login_required

def user_login(request):
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.success(request, ("Login deu errado"))
            return redirect('login')
    
    return render(request, 'authenticate\login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')
    
    
def register_user(request):
    if request.method == "POST":
        try:
            form = UserCreationForm(request.POST)
            if form.is_valid:
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(request, username=username, password=password)
                login(request, user)
                messages.success(request, 'Registro salvo')
                return redirect('index')
        except ValueError as e:
            messages.success(request, ("Seu registro deu errado"))
            return redirect('register')
    else:
        form = UserCreationForm()
    return render(request, 'authenticate/register_user.html', {'form': form,})

