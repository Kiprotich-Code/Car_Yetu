from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, CustomerRegisterForm
from django.contrib import messages

# Create your views here.
def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')               
        
        else:
            messages.error(request, 'Wrong details! Chill out, and try again!')
            return redirect('index')

    else:
        form = LoginForm()
    context = {
        'form': form
    }
        
    return render(request, 'login.html', context)


def signout(request):
    logout(request)
    return redirect('login')